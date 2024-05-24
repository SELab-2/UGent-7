import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
    base: "/docs",
    locales: {
        root: {
            label: "English",
            lang: "en",
            link: "/en",
        },
        nl: {
            label: "Nederlands",
            lang: "nl",
            link: "/nl",
        },
    },
    title: "Ypovoli",
    description: "A ugent site",
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            // { text: 'Home', link: '/en/' },
            // { text: 'Examples', link: '/markdown-examples' }
        ],

        socialLinks: [
            { icon: "github", link: "https://github.com/SELab-2/UGent-7" },
        ],
    },
})