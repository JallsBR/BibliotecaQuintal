#!/usr/bin/env bash
# Mostra os valores para colar em GitHub → Settings → Secrets → Actions
# Não versiona a chave: lê ~/.ssh/github-actions/bibliotecaquintal_deploy
set -euo pipefail
KEY="${HOME}/.ssh/github-actions/bibliotecaquintal_deploy"
if [[ ! -f "$KEY" ]]; then
  echo "Chave não encontrada: $KEY" >&2
  exit 1
fi
echo "=== VPS_HOST ==="
echo "76.13.231.242"
echo
echo "=== VPS_USER ==="
echo "root"
echo
echo "=== VPS_SSH_KEY (cole o bloco inteiro, incluindo BEGIN/END) ==="
cat "$KEY"
