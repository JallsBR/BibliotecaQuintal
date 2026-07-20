export const LOGO_BRANCO = '/bilbioteca branco alpha.png'
export const LOGO_PRETO = '/bilbioteca preto alpha.png'

export function getLogoPorTema(tema = 'claro') {
  return tema === 'escuro' ? LOGO_PRETO : LOGO_BRANCO
}

export function getTemaAtual() {
  return document.documentElement.getAttribute('data-tema') || localStorage.getItem('tema') || 'claro'
}

export function getLogoAtual() {
  return getLogoPorTema(getTemaAtual())
}

export function atualizarFavicon(tema = getTemaAtual()) {
  let link = document.querySelector("link[rel='icon']")
  if (!link) {
    link = document.createElement('link')
    link.rel = 'icon'
    document.head.appendChild(link)
  }
  link.type = 'image/png'
  link.href = getLogoPorTema(tema)
}
