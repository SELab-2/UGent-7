<script setup lang="ts">
import Tree from 'primevue/tree';
import Chip from 'primevue/chip';
import { useI18n } from 'vue-i18n';
import { type StructureCheck } from '@/types/StructureCheck.ts';
import { Project } from '@/types/Project.ts';

const { t } = useI18n();

const props = defineProps<{
    structureChecks: StructureCheck[];
}>();

console.log(props.structureChecks);
</script>

<template>
    <div>
        <div class="p-2">
            {{ t('views.projects.structureChecks.title') }}
        </div>
        <Tree class="w-100" selection-mode="single" :value="Project.getNodes(structureChecks)">
            <template #default="{ node }">
                <template v-if="node.obligated">
                    <div class="w-full" v-tooltip="t('views.projects.structureChecks.obligatedExtensions')">
                        <Chip
                            class="m-1"
                            :label="extension"
                            :key="extension"
                            v-for="extension in node.data.getObligatedExtensionList()"
                        />
                    </div>
                </template>
                <template v-else-if="node.blocked">
                    <div class="w-full" v-tooltip="t('views.projects.structureChecks.blockedExtensions')">
                        <Chip
                            class="m-1"
                            :label="extension"
                            :key="extension"
                            v-for="extension in node.data.getBlockedExtensionList()"
                        />
                    </div>
                </template>
                <template v-else>
                    <div class="flex align-items-center justify-content-between gap-3">
                        <span>
                            {{ node.label }}
                        </span>
                    </div>
                </template>
            </template>
        </Tree>
    </div>
</template>

<style scoped lang="scss">
.p-treenode-label {
    width: 100%;

    ul {
        width: 100%;
    }
}
</style>
