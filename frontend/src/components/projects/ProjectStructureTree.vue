<script setup lang="ts">
import Tree from 'primevue/tree';
import Button from 'primevue/button';
import Chips from 'primevue/chips';
import InputText from 'primevue/inputtext';
import { StructureCheck } from '@/types/StructureCheck.ts';
import { computed, ref } from 'vue';
import { type TreeNode } from 'primevue/treenode';
import { PrimeIcons } from 'primevue/api';

/* Models */
const structureChecks = defineModel<StructureCheck[]>();

/* State */
const selectedStructureCheck = ref<StructureCheck | null>(null);
const editingStructureCheck = ref<StructureCheck | null>(null);
const selectedKeys = ref<string[]>([]);
const expandedKeys = ref<string[]>([]);

/* Computed */
const nodes = computed<TreeNode[]>(() => {
    const nodes: TreeNode[] = [];

    if (structureChecks.value !== undefined) {
        for (const [i, check] of structureChecks.value.entries()) {
            const hierarchy = check.getDirectoryHierarchy();
            let currentNodes = nodes;

            for (const [j, part] of hierarchy.entries()) {
                let node = currentNodes.find((node) => node.label === part);

                if (node === undefined) {
                    node = newTreeNode(check, `${i}${j}`, part, j === hierarchy.length - 1);
                    currentNodes.push(node);
                }

                currentNodes = node.children ?? [];
            }
        }
    }

    return nodes;
});

/**
 * Delete a structure check from the list.
 *
 * @param check
 */
function deleteStructureCheck(check: StructureCheck): void {
    editingStructureCheck.value = null;
    selectedStructureCheck.value = null;

    if (structureChecks.value !== undefined) {
        const index = structureChecks.value.findIndex((c) => c === check);
        structureChecks.value.splice(index, 1);
    }
}

/**
 * Update the name of the structure check.
 *
 * @param input
 */
function updateStructureCheckName(input: HTMLInputElement): void {
    if (editingStructureCheck.value !== null && structureChecks.value !== undefined) {
        const editing: StructureCheck = editingStructureCheck.value;
        const oldPath: string = editing.path;

        editing.setLastFolderName(input.value);

        if (input.value !== '') {
            // Update the children paths.
            const children = structureChecks.value.filter((check) => check.path.startsWith(oldPath));

            for (const check of children) {
                check.path = check.path.replace(oldPath, editing.path);
            }
        }

        editingStructureCheck.value = null;
    }
}

/**
 * Add a new structure check to the list.
 */
function addStructureCheck(check: StructureCheck | null = null): void {
    if (structureChecks.value === undefined) {
        return;
    }

    if (check !== null) {
        structureChecks.value.push(check);
    } else if (editingStructureCheck.value === null) {
        let hierarchy: string[] = [];

        if (selectedStructureCheck.value !== null) {
            hierarchy = selectedStructureCheck.value.getDirectoryHierarchy();
        }

        hierarchy.push('new');

        structureChecks.value.push((editingStructureCheck.value = new StructureCheck('', hierarchy.join('/'))));
    }
}

/**
 * Select a tree node.
 *
 * @param node
 */
function selectStructureCheck(node: TreeNode): void {
    if (node.check === true) {
        selectedStructureCheck.value = node.data;
    }
}

/**
 * Construct a tree node from a structure check folder path.
 *
 * @param check
 * @param key
 * @param label
 * @param leaf
 */
function newTreeNode(check: StructureCheck, key: string, label: string, leaf: boolean = false): TreeNode {
    const node: TreeNode = {
        key,
        label,
        data: check,
        icon: PrimeIcons.FOLDER,
        check: leaf,
        children: [],
    };

    if (leaf) {
        node.children = [
            {
                key: key + '-obligated',
                icon: PrimeIcons.CHECK_CIRCLE,
                data: check,
                obligated: true,
            },
            {
                key: key + '-blocked',
                icon: PrimeIcons.TIMES_CIRCLE,
                data: check,
                blocked: true,
            },
        ];
    }

    return node;
}
</script>

<template>
    <div>
        <Tree
            class="w-100"
            selection-mode="single"
            v-model:selection-keys="selectedKeys"
            v-model:expanded-keys="expandedKeys"
            :value="nodes"
            @node-select="selectStructureCheck"
        >
            <template #default="{ node }">
                <template v-if="node.obligated">
                    <Chips
                        class="w-full"
                        :model-value="node.data.getObligatedExtensionList()"
                        @update:model-value="node.data.setObligatedExtensionList($event)"
                        v-tooltip="'Verplichte extensies'"
                    >
                        <template #chip="{ value }">
                            {{ value }}
                        </template>
                    </Chips>
                </template>
                <template v-else-if="node.blocked">
                    <Chips
                        class="w-full"
                        :model-value="node.data.getBlockedExtensionList()"
                        @update:model-value="node.data.setBlockedExtensionList($event)"
                        v-tooltip="'Verboden extensies'"
                    >
                        <template #chip="{ value }">
                            {{ value }}
                        </template>
                    </Chips>
                </template>
                <template v-else>
                    <div class="flex align-items-center justify-content-between gap-3">
                        <template v-if="node.check && editingStructureCheck === node.data">
                            <InputText
                                :model-value="node.label"
                                @change="updateStructureCheckName($event.target as HTMLInputElement)"
                                @keydown.enter="updateStructureCheckName($event.target as HTMLInputElement)"
                            >
                            </InputText>
                        </template>
                        <template v-else-if="node.check">
                            <span @click="editingStructureCheck = node.data">
                                {{ node.label }}
                            </span>
                        </template>
                        <template v-else>
                            <span>
                                {{ node.label }}
                            </span>
                        </template>
                        <span
                            v-if="structureChecks !== undefined"
                            :class="PrimeIcons.TRASH"
                            class="text-red-900 mr-2"
                            @click="deleteStructureCheck(node.data)"
                        >
                        </span>
                    </div>
                </template>
            </template>
        </Tree>

        <div class="flex justify-content-end gap-3 mt-3">
            <Button
                :icon="PrimeIcons.TIMES"
                v-if="selectedStructureCheck !== null"
                severity="contrast"
                :label="'Deselecteer ' + selectedStructureCheck.path"
                @click="
                    selectedStructureCheck = null;
                    editingStructureCheck = null;
                "
                outlined
                rounded
            />
            <Button label="Nieuwe map" :icon="PrimeIcons.FOLDER" @click="addStructureCheck()" outlined rounded link />
        </div>
    </div>
</template>

<style lang="scss">
.p-treenode-label {
    width: 100%;

    ul {
        width: 100%;
    }
}
</style>
