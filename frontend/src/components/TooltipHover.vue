<script setup lang="ts">
import { useI18n } from 'vue-i18n';

const props = defineProps<{ text: string }>();
const { t } = useI18n();
</script>

<template>
    <div class="tooltip-container">
        <!-- Tooltip text-->
        <div class="tooltip">
            <slot />
            <span class="tooltiptext">{{ t(props.text) }}</span>
        </div>
    </div>
</template>

<style scoped lang="scss">
.tooltip {
    position: relative;
    display: inline-block;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 120px;
    background-color: black;
    color: #fff;
    text-align: center;
    padding: 5px 0;
    border-radius: 6px;
    position: absolute;
    z-index: 1;
    bottom: 100%;
    left: 50%;
    margin-left: -60px;
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
