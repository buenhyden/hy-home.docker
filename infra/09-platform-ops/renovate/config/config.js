module.exports = {
    platform: 'github',

    repositories: [
        'buenhyden/hy-home.docker',
    ],

    requireConfig: 'required',
    onboarding: false,

    allowedCommands: [
        '^bash scripts/operations/sync-tech-stack-versions\\.sh --write$',
        '^bash scripts/operations/sync-update-ledger\\.sh --write$',
    ],

    allowScripts: false,
};
