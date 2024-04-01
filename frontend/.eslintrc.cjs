module.exports = {
    "env": {
        "browser": true,
        "es2021": true
    },
    "extends": [
        "standard-with-typescript",
        "plugin:vue/vue3-essential",
        "plugin:prettier/recommended"
    ],
    "overrides": [
        {
            "env": {
                "node": true
            },
            "files": [
                ".eslintrc.{js,cjs}"
            ],
            "parserOptions": {
                "sourceType": "script",
            },
        }
    ],
    "parser": "vue-eslint-parser",
    "parserOptions": {
        "parser": "@typescript-eslint/parser" ,
        "ecmaVersion": "latest",
        "sourceType": "module",
        "project": ["./tsconfig.json"],
        "extraFileExtensions": [".vue"]
    },
    "plugins": [
        "vue",
        "prettier"
    ],
    "rules": {
        "vue/multi-word-component-names": "off",  // Disable rule that requires multi-word component names in Vue files
        "@typescript-eslint/no-floating-promises": "off", // Disable rule that flags floating promises in .ts files
        "@typescript-eslint/no-extraneous-class": "off", // Disable rule that flags usage of unnecessary classes in the codebase
        "@typescript-eslint/unbound-method": "off", // Disable rule that refuses unboud methods that could scope `this`
        "prettier/prettier": "error"
    }
}
