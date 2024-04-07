<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import {useI18n} from 'vue-i18n';
import {onMounted} from "vue";
import {useProject} from "@/composables/services/project.service.ts";
import {useRoute} from "vue-router";
import {useCourses} from "@/composables/services/courses.service.ts";
import FileUpload from 'primevue/fileupload';

const {t} = useI18n();
const route = useRoute();
const {project, getProjectByID } = useProject();
const { course, getCourseByID } = useCourses();

onMounted(async () => {
  await getProjectByID(route.params.projectId as string)
  await getCourseByID(route.params.courseId as string)
});

const onUpload = (event: any) => {
  console.log(event)
}

function formatDate(deadline: Date): string {
  // changes deadline format to dd/mm.yyyy
  return `${deadline.getDate()}/${deadline.getMonth() + 1}/${deadline.getFullYear()}`;
}

</script>

<template>
  <BaseLayout>
    <div class="grid">
      <div class="col-12 md:col-4">
        <div>
          <Title>
            {{ t(`views.submissions.title`) }}: {{ project ? project.name : "Loading" }}
          </Title>
          <p v-if="course">
            {{ t(`views.submissions.course`) }}: {{ course.name }}
          </p>
          <p v-if="project?.deadline">
            Deadline: {{ project ? formatDate(project.deadline) : "Loading" }}
          </p>
          <div class="py-2">
            <h1>
              {{ t(`views.submissions.submit`) }}
            </h1>
            <FileUpload mode="basic" :multiple="true" :chooseLabel="t(`views.submissions.chooseFile`)" @upload="onUpload">

            </FileUpload>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<style scoped lang="scss">
@import '@/assets/scss/theme/theme.scss';
h1 {
  color: $primaryDarkColor
}
</style>
