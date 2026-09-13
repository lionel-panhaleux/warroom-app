# Deploy

Ships the local build to [warroom.krcg.org](https://warroom.krcg.org) and serves
it with nginx, using the `nginx_site` role from
[server-setup](https://github.com/lionel-panhaleux/server-setup). The host is
`strasbourg` in server-setup's `deploy-targets.yml`.

From this `ansible/` directory:

```bash
(cd .. && npm ci && npm run build)
ansible-galaxy collection install -r requirements.yml
ansible-playbook deploy.yml -i "HOST," --user deploy --private-key ~/.ssh/deploy --check --diff  # dry run
ansible-playbook deploy.yml -i "HOST," --user deploy --private-key ~/.ssh/deploy
```

The playbook refuses to run without `dist/index.html`; it deploys whatever is
built, so build first.

CI does the same on every push to `main` (and on demand from the Actions tab):
[`deploy.yml`](../.github/workflows/deploy.yml) builds, then runs this playbook
with `DEPLOY_SSH_KEY` (secret), `DEPLOY_HOST` and `DEPLOY_HOST_KEY` (variables)
from the `production` environment.

The first run takes the site over from the legacy `myserver` deploy: it removes
that deploy's vhosts and content directory, and `nginx_site` re-issues the
certificate through its own ACME webroot (a dry run shows that as a certbot
`--force-renewal`).
