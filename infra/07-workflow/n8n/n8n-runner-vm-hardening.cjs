'use strict';
// Preloaded into the n8n JavaScript task runner with --require (SPEC-0212
// TSK-0118 E17). The runner evaluates Code nodes in vm contexts created
// without codeGeneration, and Node then allows eval and new Function there
// whatever --disallow-code-generation-from-strings says for the main context.
// Every context the runner creates now refuses code generation from strings.
const vm = require('node:vm');

const createContext = vm.createContext;
vm.createContext = function hardenedCreateContext(contextObject, options) {
  return createContext.call(this, contextObject, {
    ...options,
    codeGeneration: { ...(options && options.codeGeneration), strings: false },
  });
};
