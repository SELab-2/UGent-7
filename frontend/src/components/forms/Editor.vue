<script setup lang="ts">
import Editor from 'primevue/editor';

const model = defineModel<string>();
</script>

<template>
    <Editor editorStyle="min-height: 250px" id="editor" v-model="model">
        <template v-slot:toolbar>
            <span class="ql-formats">
                <select class="ql-header"></select>
                <select class="ql-size"></select>
            </span>
            <span class="ql-formats">
                <button class="ql-list" value="ordered"></button>
                <button class="ql-list" value="bullet"></button>
                <button class="ql-indent" value="-1"></button>
                <button class="ql-indent" value="+1"></button>
            </span>
            <span class="ql-formats">
                <button class="ql-bold"></button>
                <button class="ql-italic"></button>
                <button class="ql-underline"></button>
                <button class="ql-strike"></button>
                <button class="ql-blockquote"></button>
            </span>
        </template>
    </Editor>
</template>

<style lang="scss">
.ql-editor {
    font-size: 16px;

    p,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        margin-bottom: 1rem !important;
    }

    ul, ol {
        margin: 1rem 0;

        li {
            margin-bottom: .5rem;
        }
    }
}
</style>
