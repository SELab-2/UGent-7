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
/* structureChecks.value = [
    new StructureCheck('', 'src', [new FileExtension('ts')], [new FileExtension('out')]),
    new StructureCheck(
        '',
        'src/controllers',
        [new FileExtension('php'), new FileExtension('java')],
        [new FileExtension('build')],
    ),
]; */

/* State */
const selectedStructureCheck = ref<StructureCheck | null>(null);
const editingStructureCheck = ref<StructureCheck | null>(null);
const selectedKeys = ref<string[]>([]);

/* Computed */
const nodes = computed<TreeNode[]>(() => {
    const nodes: TreeNode[] = [];

    if (structureChecks.value !== undefined) {
        for (const check of structureChecks.value) {
            const hierarchy = check.getDirectoryHierarchy();
            let currentNodes = nodes;

            for (const [i, part] of hierarchy.entries()) {
                let node = currentNodes.find((node) => node.key === part);

                if (node === undefined) {
                    node = newTreeNode(check, part, i === hierarchy.length - 1);
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
    if (editingStructureCheck.value !== null) {
        if (input.value === '') {
            deleteStructureCheck(editingStructureCheck.value);
        } else {
            editingStructureCheck.value.setLastFolderName(input.value);
        }
    }
}

/**
 * Add a new structure check to the list.
 */
function addStructureCheck(): void {
    if (structureChecks.value !== undefined) {
        let hierarchy: string[] = [];

        if (selectedStructureCheck.value !== null) {
            hierarchy = selectedStructureCheck.value.getDirectoryHierarchy();
        }

        hierarchy.push('new');

        structureChecks.value.push((editingStructureCheck.value = new StructureCheck('', hierarchy.join('/'))));
    }
}

/**
 * Construct a tree node from a structure check folder path.
 *
 * @param check
 * @param part
 * @param leaf
 */
function newTreeNode(check: StructureCheck, part: string, leaf: boolean = false): TreeNode {
    const node: TreeNode = {
        key: part,
        label: part,
        data: check,
        icon: PrimeIcons.FOLDER,
        check: leaf,
        children: [],
    };

    if (leaf) {
        node.children = [
            {
                key: part + '-obligated',
                icon: PrimeIcons.CHECK_CIRCLE,
                data: check,
                obligated: true,
            },
            {
                key: part + '-blocked',
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
    <Tree
        class="w-100"
        selection-mode="single"
        v-model:selection-keys="selectedKeys"
        :value="nodes"
        @node-select="selectedStructureCheck = $event.data"
    >
        <template #default="{ node }">
            <template v-if="node.obligated">
                <Chips
                    class="w-full"
                    :model-value="node.data.getObligatedExtensionList()"
                    @update:model-value="node.data.setObligatedExtensionList($event)"
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
                            @blur="editingStructureCheck = null"
                            @keydown.enter="
                                updateStructureCheckName($event.target as HTMLInputElement);
                                editingStructureCheck = null;
                            "
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
                    <Button
                        v-if="structureChecks !== undefined"
                        severity="danger"
                        :icon="PrimeIcons.TRASH"
                        @click="deleteStructureCheck(node.data)"
                        rounded
                        outlined
                    >
                    </Button>
                </div>
            </template>
        </template>
    </Tree>
    <div class="flex justify-content-end mt-3">
        <Button label="Nieuwe map" :icon="PrimeIcons.FOLDER" @click="addStructureCheck" rounded />
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
