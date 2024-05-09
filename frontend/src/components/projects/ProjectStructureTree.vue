<script setup lang="ts">
import Tree from 'primevue/tree';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import { StructureCheck } from '@/types/StructureCheck.ts';
import { computed, ref } from 'vue';
import { type TreeNode } from 'primevue/treenode';

/* Models */
const structureChecks = defineModel<StructureCheck[]>();

/* State */
const selectionKeys = ref(undefined);
const selectedNode = ref<TreeNode | null>(null);
const newStructureCheck = ref<StructureCheck | null>(null);

const nodes = computed<TreeNode[]>(() => {
    const nodes: TreeNode[] = [];
    const checks: StructureCheck[] = [...(structureChecks.value ?? [])];

    if (newStructureCheck.value) {
        checks.push(newStructureCheck.value);
    }

    checks.forEach((structureCheck: StructureCheck) => {
        const hierarchy = structureCheck.getDirectoryHierarchy();
        let currentNodes = nodes;

        for (const [i, directory] of hierarchy.entries()) {
            let node = currentNodes.find(node => node.label === directory);

            if (node === undefined) {
                const leaf = i + 1 === hierarchy.length;

                currentNodes.push(node = {
                    leaf,
                    icon: leaf ? '' : 'pi-folder',
                    label: directory,
                    children: [],
                    data: leaf ? structureCheck : null
                });
            }

            currentNodes = node.children ?? [];
        }
    });

    return nodes;
});

function addStructureCheck() {
    if (newStructureCheck.value === null) {
        let path = '';

        if (selectedNode.value !== null) {
            console.log(selectedNode.value);
        }

        newStructureCheck.value = new StructureCheck(
            '', path
        );
    }
}
</script>

<template>
    <div class="flex justify-content-between align-items-center mb-3">
        <span>Indieningsstructuur</span>
        <Button icon="pi pi-folder" @click="addStructureCheck" rounded />
    </div>
    <Tree :value="nodes" class="w-100" selection-mode="single" v-model:selection-keys="selectionKeys"
          @node-select="selectedNode = $event" @node-unselect="selectedNode = null">
        <template #default="{ node }">
            <template v-if="node.leaf">
                <template v-if="!node.data.exists()">
                    <InputText v-model="newStructureCheck.path" v-if="newStructureCheck"/>
                </template>
            </template>
        </template>
    </Tree>
</template>

<style scoped lang="scss"></style>
