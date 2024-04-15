<script setup lang="ts">
import Editor from 'primevue/editor';
import Button from 'primevue/button';

const model = defineModel();
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

<style scoped lang="scss"></style>
