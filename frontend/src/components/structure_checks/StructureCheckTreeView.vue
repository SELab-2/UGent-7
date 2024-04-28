<script setup lang="ts">
import { useStructureCheck } from '@/composables/services/structure_check.service';
import Tree from 'primevue/tree';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { parseArgs } from 'util';
import { StructureCheck } from '@/types/StructureCheck';

/* Props */
const props = defineProps<{
    projectId: string;
    editable: boolean;
}>();

const { t } = useI18n();

const { structureChecks, getStructureCheckByProject, createStructureCheck, deleteStructureCheck } = useStructureCheck();

onMounted(() => {
    loadStructureChecks();
});

interface TreeNode_struct {
    label: string;
    children?: TreeNode_struct[];
    key: string;
    sort: string;
    parrent: TreeNode_struct | null; // TODO is this needed
}

// Define a method to compute the style for each node
function getNodeStyle(node: TreeNode_struct) {
    // Check if the node meets a certain condition, e.g., has a specific label
    if (node.sort === 'file') return { color: 'black' };
    if (node.sort === 'obligated') return { color: 'green' };
    if (node.sort === 'blocked') return { color: 'red' };
    // If no condition is met, return an empty object
    return {};
}

// Define tree data as ref
const nodes = ref<TreeNode_struct[]>([]);

type StringToIntDict = Record<string, number>;

// Function to load structure checks into nodes
async function loadStructureChecks() {
    await getStructureCheckByProject(props.projectId); // 3001

    // Initialize an empty array for the result
    const result: TreeNode_struct[] = [];

    // Initialize a level object with the result array
    const level = { result };

    // Iterate over each path
    (structureChecks.value || []).forEach((structureCheck) => {
        let path = structureCheck.name;
        const obligated = structureCheck.obligated_extensions;
        const blocked = structureCheck.blocked_extensions;

        if (path === '.') {
            path = '';
        } else if (!path.startsWith('/')) {
            path = '/' + path;
        }

        // Split the path into individual parts
        let parrent: TreeNode_struct | null = null;
        path.split('/').reduce((r: any, name: string, i: number, a: string[]) => {
            // Check if the current part doesn't exist in the hierarchy
            if (!r[name]) {
                // Create a new node for the current part
                r[name] = { result: [] };
                // Add the node to the result array
                const newNode: TreeNode_struct = {
                    key: `${path}_${name}_${i}`,
                    label: name,
                    children: r[name].result,
                    sort: 'file',
                    parrent,
                };
                parrent = newNode;

                // Add the node to the parent's children array
                r.result.push(newNode);

                if (i === a.length - 1) {
                    if (obligated) {
                        // If it's the deepest path and there are obligated extensions, add them as children
                        obligated.forEach((ext: any, index: number) => {
                            r[name].result.push({
                                key: `${path}_${name}_obligated_${index}`,
                                label: ext.extension,
                                sort: 'obligated',
                                parrent: newNode,
                            });
                        });
                    }
                    if (blocked) {
                        // If it's the deepest path and there are blocked extensions, add them as children
                        blocked.forEach((ext: any, index: number) => {
                            r[name].result.push({
                                key: `${path}_${name}_blocked_${index}`,
                                label: ext.extension,
                                sort: 'blocked',
                                parrent: newNode,
                            });
                        });
                    }
                }
            }
            // Return the current node
            return r[name];
        }, level);
    });

    // Assign the fetched data to the nodes
    if (result[0]) {
        nodes.value = result[0].children || [];
    }
}

const editedNode = ref<TreeNode_struct | null>(null);
const editedNodeName = ref('');
interface DropdownOption {
    label: string;
    value: string;
}
const obligatedOption: DropdownOption = {
    label: 'Obligated',
    value: 'obligated',
};
const blockedOption: DropdownOption = {
    label: 'Blocked',
    value: 'blocked',
};
const fileOption: DropdownOption = {
    label: 'File',
    value: 'file',
};
const nodeTypes: DropdownOption[] = [fileOption, obligatedOption, blockedOption];
const editedNodeType = ref<DropdownOption>(nodeTypes[0]);

const onNodeSelect = (event: TreeNode_struct) => {
    editedNode.value = event;
};

const unselectNode = (event: TreeNode_struct) => {
    editedNode.value = null;
};

const editSelectedNode = () => {
    if (editedNode.value && editedNode.value.sort != 'empty') {
        editedNode.value.label = editedNodeName.value;
    }
};

let counter = 0;
const addSelectedNode = () => {
    if (editedNode.value?.children) {
        if (editedNode.value.sort != 'empty') {
            counter += 1;
            const node: TreeNode_struct = {
                key: `${editedNode.value.label}_${counter}_obligated_${editedNodeName.value}`,
                label: editedNodeName.value,
                sort: editedNodeType.value.value,
                children: [],
                parrent: editedNode.value,
            };
            editedNode.value.children.push(node);
            // sort the nodes by type to make them cluster together
            editedNode.value.children.sort((a: TreeNode_struct, b: TreeNode_struct) => {
                const order: StringToIntDict = { obligated: 0, blocked: 1, file: 2 };
                return order[a.sort] - order[b.sort];
            });
        }
    } else {
        const node: TreeNode_struct = {
            key: `_${counter}_obligated_${editedNodeName.value}`,
            label: editedNodeName.value,
            sort: editedNodeType.value.value,
            children: [],
            parrent: null,
        };
        nodes.value.push(node);
    }
};

const deleteSelectedNode = () => {
    if (editedNode.value) {
        if (editedNode.value.sort != 'empty') {
            // Find the index of the selected node in the parent's children array
            if (editedNode.value.parrent?.children) {
                const index = editedNode.value.parrent.children.findIndex((child) => child === editedNode.value);

                // If the selected node is found in the parent's children array
                if (index !== -1) {
                    // Remove the selected node from the parent's children array
                    editedNode.value.parrent.children.splice(index, 1);
                }
            } else {
                console.log('root');
                const index = nodes.value.findIndex((child) => child === editedNode.value);

                // If the selected node is found in the parent's children array
                if (index !== -1) {
                    // Remove the selected node from the parent's children array
                    nodes.value.splice(index, 1);
                }
            }
        }
    }
};

async function saveSelectedNode() {
    const checks = parseNodesToStructureChecks(nodes.value);
    console.log(checks);
    await getStructureCheckByProject(props.projectId);
    if (structureChecks.value) {
        await Promise.all(
            structureChecks.value.map(async (check) => {
                await deleteStructureCheck(check.id);
            }),
        );
    }
    console.log(structureChecks);
    // TODO pack into 1 call
    await Promise.all(
        checks.map(async (check) => {
            await createStructureCheck(check, props.projectId);
        }),
    );
}

function parseNodesToStructureChecks(nodes: TreeNode_struct[]): any[] {
    const structureChecks: any[] = [];

    // Recursive function to traverse tree nodes and build structure checks
    function traverse(node: TreeNode_struct, parentPath: string = '') {
        // Generate the full path by concatenating parent paths and current node label
        let fullPath;
        if (node.sort == 'file') {
            fullPath = parentPath === '' ? node.label : `${parentPath}/${node.label}`;
        } else {
            fullPath = parentPath;
        }

        // Search for an existing structure check with the same name as fullPath
        let structureCheck = structureChecks.find((check) => check.name === fullPath);

        // If no existing structure check is found, create a new one
        if (!structureCheck) {
            structureCheck = {
                name: fullPath,
                obligated_extensions: [],
                blocked_extensions: [],
                // Add other properties as needed
            };
            structureChecks.push(structureCheck);
        }

        // Add obligated and blocked extensions if they exist for the current node
        if (node.sort === 'obligated' && node.label !== '.') {
            structureCheck.obligated_extensions.push({ extension: node.label });
        } else if (node.sort === 'blocked' && node.label !== '.') {
            structureCheck.blocked_extensions.push({ extension: node.label });
        }

        // Recursively traverse children
        if (node.children) {
            node.children.forEach((child) => {
                traverse(child, fullPath);
            });
        }
    }

    // Start traversing from the root nodes
    nodes.forEach((node) => {
        traverse(node);
    });

    return structureChecks;
}
</script>

<template>
    <Tree
        v-if="nodes && nodes.length"
        :value="nodes"
        class="w-full md:w-30rem"
        @node-select="onNodeSelect"
        selectionMode="single"
    >
        <template #default="node">
            <b :style="getNodeStyle(node.node)">{{ node.node.label }}</b>
        </template>
    </Tree>
    <Button
        v-if="$props.editable"
        :label="t('structure_checks.reload')"
        type="button"
        icon="pi pi-refresh"
        iconPos="right"
        @click="loadStructureChecks"
        rounded
    />

    <InputText v-if="$props.editable" v-model="editedNodeName" placeholder="Edit Node Name" />

    <Button
        v-if="$props.editable"
        :label="t('structure_checks.edit')"
        type="button"
        icon="pi pi-refresh"
        iconPos="right"
        @click="editSelectedNode"
        rounded
    />

    <Button
        v-if="$props.editable"
        :label="t('structure_checks.add')"
        type="button"
        icon="pi pi-refresh"
        iconPos="right"
        @click="addSelectedNode"
        rounded
    />

    <Button
        v-if="$props.editable"
        :label="t('structure_checks.delete')"
        type="button"
        icon="pi pi-refresh"
        iconPos="right"
        @click="deleteSelectedNode"
        rounded
    />

    <Button
        v-if="$props.editable"
        :label="t('structure_checks.save')"
        type="button"
        icon="pi pi-refresh"
        iconPos="right"
        @click="saveSelectedNode"
        rounded
    />

    <Button
        v-if="$props.editable"
        :label="t('structure_checks.unselect')"
        type="button"
        icon="pi pi-refresh"
        iconPos="right"
        @click="unselectNode"
        rounded
    />

    <Dropdown v-if="$props.editable" v-model="editedNodeType" :options="nodeTypes" />
</template>
