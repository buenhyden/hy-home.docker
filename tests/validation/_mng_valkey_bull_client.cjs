const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = '/usr/local/lib/node_modules/n8n';
const fromN8n = require('node:module').createRequire(root + '/package.json');
const digest = (data, algorithm='sha256') => crypto.createHash(algorithm).update(data).digest('hex');
const emit = value => console.log(JSON.stringify(value));
function identityValid(i) {
  return Boolean(i.uid === 1000 && i.gid === 1000 && i.n8n?.version === '2.43.6' &&
    i.bull?.version === '4.16.4' && i.bull.entry && i.bull.entry === i.bull.expectedEntry &&
    i.bull.jobGit === '3301e3fbc7296f545b65331dad1f12c820267e0d' &&
    i.ioredis?.version === '5.3.2' && i.ioredis.entry && i.ioredis.entry === i.ioredis.expectedEntry);
}
function probeIdentity() {
  const result = {kind:'identity', node:process.version, executable:process.execPath, uid:process.getuid(), gid:process.getgid()};
  try { const raw=fs.readFileSync(root+'/package.json'); result.n8n={version:JSON.parse(raw).version,sha256:digest(raw)}; }
  catch { result.n8n={error:'UNAVAILABLE'}; }
  for (const [name, entry] of [['bull','index.js'],['ioredis','built/index.js']]) {
    const item = {};
    try {
      const file=fromN8n.resolve(name+'/package.json'); const raw=fs.readFileSync(file);
      item.version=JSON.parse(raw).version; item.packagePath=file; item.packageSha256=digest(raw);
      item.entry=fromN8n.resolve(name); item.entrySha256=digest(fs.readFileSync(item.entry));
      item.entry=fs.realpathSync(item.entry);
      item.expectedEntry=fs.realpathSync(root+'/node_modules/'+name+'/'+entry);
      if (name === 'bull') {
        const job=fs.readFileSync(path.join(path.dirname(file),'lib/job.js'));
        item.jobSha256=digest(job); item.jobGit=digest(Buffer.concat([Buffer.from('blob '+job.length+'\0'),job]),'sha1');
      }
    } catch { item.error='UNAVAILABLE_OR_UNEXPECTED_LAYOUT'; }
    result[name]=item;
  }
  emit(result);
  return result;
}
const sleep = milliseconds => new Promise(resolve => setTimeout(resolve,milliseconds));
async function bounded(promise, milliseconds=15000) {
  let timer;
  try { return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error('CASE_TIMEOUT')),milliseconds);})]); }
  finally { clearTimeout(timer); }
}
async function runPositive(queue, connect, passed, recordError) {
  const producer=queue(); const worker=queue(); let release=false; let entered;
  const active=new Promise(resolve=>{entered=resolve;});
  await bounded(Promise.all([producer.isReady(),worker.isReady()]));
  void worker.process('job',1,async job=>{
    await job.progress(42);
    if (job.data.kind==='retry' && job.attemptsMade===0) throw new Error('SYNTHETIC_RETRY');
    if (job.data.kind==='lock') { entered(); while(!release) await sleep(100); }
    return {kind:job.data.kind,attempts:job.attemptsMade,at:Date.now()};
  }).catch(recordError);
  const basic=await bounded(producer.add('job',{kind:'basic'}));
  assert.equal((await bounded(basic.finished())).kind,'basic'); assert.equal(await basic.getState(),'completed'); passed('job-worker-progress-finished');
  const retry=await bounded(producer.add('job',{kind:'retry'},{attempts:2,backoff:{type:'fixed',delay:200}}));
  assert.equal((await bounded(retry.finished())).attempts,1); passed('failed-once-retry-completed');
  const start=Date.now(); const delayed=await bounded(producer.add('job',{kind:'delay'},{delay:1000}));
  assert.equal(await delayed.getState(),'delayed'); assert.ok((await bounded(delayed.finished())).at>=start+900); passed('delayed-job-completed');
  const locked=await bounded(producer.add('job',{kind:'lock'})); await bounded(active);
  assert.equal(await locked.takeLock(),false); await assert.rejects(locked.releaseLock(),/Could not release lock/);
  let previous=await producer.client.pttl(locked.lockKey()); let renewed=false; const until=Date.now()+16000;
  while(Date.now()<until) { await sleep(200); const ttl=await producer.client.pttl(locked.lockKey()); assert.ok(ttl>0); if(ttl>previous+2000){renewed=true;break;} previous=ttl; }
  assert.ok(renewed,'worker lock did not renew'); release=true;
  assert.equal((await bounded(locked.finished())).kind,'lock'); assert.equal(await producer.client.exists(locked.lockKey()),0); passed('lock-renewal-token-isolation-release');
  const subscriber=connect(); const message=new Promise(resolve=>subscriber.once('message',(channel,value)=>resolve([channel,value])));
  await bounded(subscriber.subscribe('n8n:n8n.commands')); await producer.client.publish('n8n:n8n.commands','synthetic');
  assert.deepEqual(await bounded(message),['n8n:n8n.commands','synthetic']); passed('named-channel-pubsub');
}
function authenticationCode(error) {
  if(error?.name !== 'ReplyError') return null;
  return /^(WRONGPASS|NOAUTH)\b/.exec(error.message||'')?.[1]||null;
}
async function requireWrongPassword(wrong, milliseconds=3000) {
  let listener;
  const denial=new Promise((resolve,reject)=>{
    listener=error=>{
      const code=authenticationCode(error);
      if(code && error.command?.name==='auth') resolve(code);
      else reject(new Error('AUTH_PROBE_UNEXPECTED_ERROR'));
    };
    wrong.once('error',listener);
  });
  try {
    await bounded((async()=>{
      const connected=wrong.connect().then(()=> 'ready',()=> 'closed');
      const ping=wrong.ping().then(()=>({accepted:true}),error=>({accepted:false,code:authenticationCode(error)}));
      const code=await denial;
      assert.deepEqual(await ping,{accepted:false,code});
      await connected;
      emit({kind:'auth-denial',code,commandDenied:true});
    })(),milliseconds);
  } finally {
    wrong.removeListener('error',listener);
    wrong.disconnect();
  }
}
async function selfCheckWrongPassword() {
  const {EventEmitter}=require('node:events');
  const reply=(code='WRONGPASS',command='auth',name='ReplyError')=>
    Object.assign(new Error(code),{name,command:{name:command}});
  function fake(mode) {
    const client=new EventEmitter();
    client.on('error',()=>{});
    const auth=()=>mode==='spoof' ? new Error('WRONGPASS') :
      reply(mode==='noauth'?'NOAUTH':'WRONGPASS',mode==='wrong-command'?'get':'auth',mode==='generic-auth'?'Error':'ReplyError');
    let timer;
    client.disconnect=()=>clearTimeout(timer);
    client.connect=()=>{
      if(!['close-only','silent'].includes(mode)) {
        timer=setTimeout(()=>client.emit('error',mode==='transport'?new Error('ECONNRESET'):auth()),mode==='late'?100:0);
      }
      return mode==='close-auth'||mode==='close-only' ? Promise.reject(new Error('Connection is closed.')) : Promise.resolve();
    };
    client.ping=()=>mode==='pong' ? Promise.resolve('PONG') :
      Promise.reject(mode==='close-only'?new Error('Connection is closed.'):reply(mode==='noauth'?'NOAUTH':'WRONGPASS'));
    return client;
  }
  for(const mode of ['ready-auth','close-auth','noauth']) await requireWrongPassword(fake(mode),20);
  for(const mode of ['close-only','transport','pong','silent','late','spoof','wrong-command','generic-auth']) {
    await assert.rejects(requireWrongPassword(fake(mode),20));
  }
}
async function runNegative(connect, passed) {
  const client=connect(); await bounded(client.ping());
  for (const [name,command] of [
    ['foreign-key',['GET','other:key']],['foreign-db',['SELECT','1']],['foreign-channel',['PUBLISH','other:channel','synthetic']],
    ['flushdb',['FLUSHDB']],['flushall',['FLUSHALL']],['acl',['ACL','LIST']],['config',['CONFIG','GET','*']],['keys',['KEYS','*']],['scan',['SCAN','0']]
  ]) { await assert.rejects(bounded(client.call(...command)),/NOPERM|ACL/); passed(name); }
  const wrong=connect({password:'synthetic-wrong',lazyConnect:true,retryStrategy:()=>null,maxRetriesPerRequest:0});
  await requireWrongPassword(wrong); passed('wrong-password');
}
async function runMain() {
  const identity=probeIdentity();
  if (!identityValid(identity)) { emit({kind:'blocked',code:'BLOCKED_CLIENT_VERSION_OR_LAYOUT'}); process.exitCode=2; return; }
  const mode=process.argv[2];
  const timer=setTimeout(()=>process.exit(124),mode==='hold'?180000:45000);
  if (mode === 'hold') { emit({kind:'ready'}); return; }
  const input=JSON.parse(fs.readFileSync('/fixture/input.json','utf8'));
  assert.deepEqual(Object.keys(input).sort(),['db','host','password','port','username']);
  assert.equal(input.host,'broker'); assert.equal(input.port,6379); assert.equal(input.db,0); assert.equal(input.username,'n8n');
  const Redis=fromN8n('ioredis'); const Bull=fromN8n('bull');
  let clients=[]; let queues=[]; let errors=[]; let cases=[];
  const recordError=error=>{errors=[...errors,error.code||error.name];};
  function connect(extra={}) {
    const client=new Redis({...input,enableReadyCheck:false,maxRetriesPerRequest:null,retryStrategy:()=>1000,connectTimeout:2000,...extra});
    client.on('error',()=>{}); clients=[...clients,client]; return client;
  }
  function queue() {
    const q=new Bull('jobs',{prefix:'n8n',settings:{lockDuration:60000,lockRenewTime:10000,stalledInterval:30000,maxStalledCount:0},createClient:()=>connect()});
    q.on('error',recordError); queues=[...queues,q]; return q;
  }
  const passed=name=>{cases=[...cases,name];emit({kind:'case',mode,name,status:'PASS'});};
  try {
    if (mode === 'positive') {
      await runPositive(queue, connect, passed, recordError);
      assert.deepEqual(errors,[]); assert.equal(cases.length,5);
    } else if (mode === 'negative') {
      await runNegative(connect, passed); assert.equal(cases.length,10);
    } else { throw new Error('UNKNOWN_MODE'); }
    emit({kind:'complete',mode,cases});
  } finally {
    for (const q of queues) {
      try { await bounded(q.close(true),3000); }
      catch(error) { emit({kind:'client-cleanup-error',code:error.code||error.name}); process.exitCode=1; }
    }
    for (const client of clients) client.disconnect();
    clearTimeout(timer);
  }
}
module.exports={identityValid,requireWrongPassword,selfCheckWrongPassword};
if(require.main===module) runMain().catch(error=>{emit({kind:'failure',code:error.code||error.name});process.exitCode=1;});
