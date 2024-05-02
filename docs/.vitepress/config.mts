import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  locales: {
    root: {
      label: 'English',
      lang: 'en',
      link: '/en'
    },
    nl: {
      label: 'Nederlands',
      lang: 'nl', // optional, will be added  as `lang` attribute on `html` tag
      link: '/nl' // default /fr/ -- shows on navbar translations menu, can be external

      // other locale specific properties...
    }
  },
  title: "Ypovoli",
  description: "A ugent site",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      // { text: 'Home', link: '/en/' },
      // { text: 'Examples', link: '/markdown-examples' }
    ],

    sidebar: [
      {
        text: 'Algemeen',
        items: [
          { text: 'Markdown Examples', link: '/markdown-examples' },
          { text: 'Runtime API Examples', link: '/api-examples' }
        ]
      }
    ],

    socialLinks: [
      // { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    ]
  }
})
