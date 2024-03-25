<script setup lang="ts">
import BaseLayout from "@/components/layout/BaseLayout.vue";
import {useI18n} from 'vue-i18n';
import {Project} from "@/types/Projects.ts";
import {onMounted} from "vue";
import {useProject} from "@/composables/services/project.service.ts";
import {useRoute} from "vue-router";
import Title from "@/components/Title.vue";
import Skeleton from "primevue/skeleton";

/* Composable injections */
const { t } = useI18n();
/* Service injections */
const route = useRoute();
const { project, getProjectByID } = useProject();

/* Component props */
const props = defineProps<{
  projectId: {
    type: number
  }
}>();

onMounted(async () => {
  const projectId = route.params.projectId;
  console.log(projectId);
  await getProjectByID(parseInt(projectId as string));
});

</script>

<template>
  <BaseLayout>
    <div class="grid">
      <div class="col-12 md:col-6">
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
    </div>
  </BaseLayout>
</template>

<style scoped lang="scss">

</style>