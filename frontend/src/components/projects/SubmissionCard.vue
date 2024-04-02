<script setup lang="ts">

/* Component props */
import {Project} from "@/types/Projects.ts";
import {PrimeIcons} from "primevue/api";
import Button from "primevue/button";
import Card from "primevue/card";
import {useI18n} from "vue-i18n";
import {computed} from "vue";

const { t } = useI18n();

const props = defineProps<{
  project: Project

}>();

const formattedDeadline = computed(() => {
  // changes deadline format to dd/mm.yyyy
  const date = new Date(props.project.deadline);
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
});

</script>

<template>
  <Card class="border-round project-card">
    <template #content>
     <div>
      <div class="mb-3">
        <i :class="['pi', PrimeIcons.CALENDAR_PLUS, 'icon-color']" class="mr-2"></i>
        {{t('views.projects.deadline')}}: {{ formattedDeadline }}<br>
      </div>
      <div>
        <i :class="['pi', PrimeIcons.INFO_CIRCLE, 'icon-color']" class="mr-2"></i>
        {{t('views.projects.submissionStatus')}}: {{ project.submissions.at(-1)?.structureChecks_passed }}
      </div>
     </div>
    </template>
    <template #footer>
      <RouterLink :to="{ name: 'submission', params: { submissionId: project.submissions.at(-1)?.id } }" v-if="project.submissions.at(-1)?.id">
        <Button :icon="PrimeIcons.ARROW_RIGHT" :label="t('components.submission')" icon-pos="right" outlined/>
      </RouterLink>
    </template>
  </Card>
</template>

<style scoped lang="scss">

</style>