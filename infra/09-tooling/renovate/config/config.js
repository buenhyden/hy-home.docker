module.exports = {
    platform: 'github',

    repositories: [
        'buenhyden/hy-home.docker',
    ],

    requireConfig: 'required',
    onboarding: false,

    allowedCommands: [
        '^bash scripts/operations/sync-tech-stack-versions\\.sh$',
    ],

    allowScripts: false,
};
