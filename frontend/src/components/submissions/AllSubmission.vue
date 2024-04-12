<script setup lang="ts">
import { ref, computed } from 'vue';
import { Submission } from "@/types/Submission.ts";
import { Group } from "@/types/Group.ts";
import LanguageSelector from "@/components/LanguageSelector.vue";

const props = defineProps<{
  group: Group;
}>();

const submissions = ref<Submission[]>([
  new Submission('1', 1, new Date(2024, 4, 8), true, props.group, [], []),
  new Submission('2', 2, new Date(2024, 4, 8), false, props.group, [], []),
  new Submission('3', 3, new Date(2024, 4, 9), true, props.group, [], []),
  new Submission('4', 4, new Date(2024, 4, 9), false, props.group, [], []),
  new Submission('5', 5, new Date(2024, 4, 10), true, props.group, [], []),
]);

const enhancedSubmissions = computed(() => {
  const result = submissions.value.map(submission => {
    const iconDetails = getIcon(submission);
    return {
      ...submission,
      iconName: iconDetails.iconName,
      color: iconDetails.color,
    };
  });
  console.log(result)
  return result;
});

const getIcon = (submission: Submission): { iconName: string; color: string } => {
  if (!(submission.extra_checks_results.every(Boolean) || submission.structure_checks_passed)) {
    return { iconName: 'times', color: 'red' };
  } else if (!submission.extra_checks_results.every(Boolean)) {
    return { iconName: 'cloud', color: 'red' };
  } else if (!submission.structure_checks_passed) {
    return { iconName: 'bolt', color: 'red' };
  } else {
    return { iconName: 'check', color: 'lightgreen' };
  }
}

</script>

<template>
  <div>
    <div v-for="submission in enhancedSubmissions" class="flex submission align-content-center align-items-center">
      <p :class="'font-semibold m-2 p-1 pi pi-' + submission.iconName" :style="{color: submission.color, fontSize: '1.25rem'}"></p>
      <label>#{{ submission.submission_number}}</label>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/theme/theme.scss';
.submission {
  border-bottom: 1.5px solid black;
}
.submission:last-child {
  border-bottom: none;
}
</style>