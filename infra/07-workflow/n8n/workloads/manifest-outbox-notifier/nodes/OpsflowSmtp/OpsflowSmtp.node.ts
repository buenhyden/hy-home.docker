import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';
import type { IExecuteFunctions, INodeExecutionData, INodeType, INodeTypeDescription } from 'n8n-workflow';
import { sendClaim, validateClaim } from './transport';

export class OpsflowSmtp implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Opsflow SMTP Capture', name: 'opsflowSmtp',
    group: ['output'], version: 1,
    description: 'Restricted draft DEV manifest outbox Mailpit capture',
    defaults: { name: 'Opsflow SMTP Capture' },
    inputs: [NodeConnectionTypes.Main], outputs: [NodeConnectionTypes.Main],
    credentials: [{ name: 'smtp', required: true }],
    properties: [{ displayName: 'Closed Claim', name: 'claim', type: 'json', default: '{}',
      required: true, description: 'Validated closed claim object from the native Postgres node' }],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    try {
      const items = this.getInputData();
      if (items.length === 0) return [[]];
      if (items.length !== 1 || items[0].binary) throw new Error('OPSFLOW_INVALID_INPUT');
      const claim = validateClaim(this.getNodeParameter('claim', 0));
      let credential: unknown;
      try { credential = await this.getCredentials('smtp'); }
      catch { throw new Error('OPSFLOW_CREDENTIAL_UNAVAILABLE'); }
      const outcome = await sendClaim(claim, credential, this.getExecutionCancelSignal());
      return [[{ json: { run_id: outcome.run_id, state: outcome.state }, pairedItem: { item: 0 } }]];
    } catch (error) {
      const allowed = ['OPSFLOW_INVALID_INPUT', 'OPSFLOW_INVALID_CLAIM', 'OPSFLOW_INVALID_CREDENTIAL', 'OPSFLOW_CREDENTIAL_UNAVAILABLE'];
      const code = error instanceof Error && allowed.includes(error.message) ? error.message : 'OPSFLOW_NODE_FAILED';
      // Never attach the driver error, input object or credential to n8n error data.
      throw new NodeOperationError({
        id: 'opsflow-smtp-capture', name: 'Opsflow SMTP Capture',
        type: 'n8n-nodes-opsflow.opsflowSmtp', typeVersion: 1,
        position: [0, 0], parameters: {},
      }, code);
    }
  }
}
