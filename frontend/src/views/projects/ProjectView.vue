<script setup lang="ts">
import BaseLayout from "@/components/layout/BaseLayout.vue";
import {useI18n} from 'vue-i18n';
import {onMounted, ref} from "vue";
import {useProject} from "@/composables/services/project.service.ts";
import {useRoute} from "vue-router";
import Title from "@/components/Title.vue";
import Skeleton from "primevue/skeleton";
import GroupCard from "@/components/projects/GroupCard.vue";
import {useGroup} from "@/composables/services/groups.service.ts";
import {Group} from "@/types/Group.ts";
import SubmissionCard from "@/components/projects/SubmissionCard.vue";

/**
 * Todo change all static id's to user.id
 */

/* Composable injections */
const { t } = useI18n();
/* Service injections */
const route = useRoute();
const { project, getProjectByID } = useProject();
const { groups, getGroupsByProject, getGroupsByStudent } = useGroup();
const finalGroup = ref<Group>(new Group("-1"));

onMounted(async () => {
  const projectId = route.params.projectId;
  await getProjectByID(projectId as string);
  console.log("fetching groups")
  // Get id group from project by comparing the users groups and the project groups
  await getGroupsByProject(projectId as string);
  const projectGroups = groups.value;
  // get all groups from the user
  await getGroupsByStudent("1");
  for (const group of groups.value ?? []) {
    const isCommonGroup = projectGroups?.some(projectGroup => projectGroup.id === group.id);

    if (isCommonGroup) {
      finalGroup.value = group;
      break;
    }
  }
});

</script>

<template>
  <BaseLayout>
    <div class="grid">
      <div class="col-12 md:col-8">
        <div>
          <Title v-if="project">
            {{ project.name }}
          </Title>
          <Skeleton class="mb-4" height="3rem" width="30rem" v-else/>
        </div>
        <div>
          <p v-if="project">
            {{ project.description }}
          </p>
          <Skeleton height="10rem" v-else/>
        </div>
      </div>
      <div class="col-12 md:col-4">
        <SubmissionCard v-if="project" :project="project" style="margin-bottom: 20px;"></SubmissionCard>
        <GroupCard v-if="finalGroup.id !== '-1'" :group-id="finalGroup.id"></GroupCard>
      </div>
    </div>
  </BaseLayout>
</template>

<style scoped lang="scss">

</style>