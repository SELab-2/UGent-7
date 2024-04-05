<script setup lang="ts">
import Card from 'primevue/card';
import Button from 'primevue/button';
import { type Project } from '@/types/Projects.ts';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';
import moment from 'moment';
import { type Course } from '@/types/Course.ts';

/**
 * TODO
 *  - Submission check depends on more than just structure checks
 */

/* Component props */
const props = defineProps<{
    project: Project;
    course: Course;
}>();

const formattedDeadline = computed(() => {
    return moment(props.project.deadline).format('DD MMMM YYYY');
});

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <Card class="border-round project-card">
        <template #header>
            <h2 class="text-primary m-0 text-xl"><span class="pi pi-book text-xl mr-2" /> {{ course.name }}</h2>
        </template>
        <template #subtitle>
            {{ project.name }}
        </template>
        <template #content>
            <div class="mb-2">
                <i :class="['pi', PrimeIcons.CALENDAR_PLUS, 'icon-color']" class="mr-2"></i>
                {{ t('views.projects.deadline') }}: {{ formattedDeadline }}<br />
            </div>
            <div>
                <i :class="['pi', PrimeIcons.INFO_CIRCLE, 'icon-color']" class="mr-2"></i>
                {{ t('views.projects.submissionStatus') }}: ok
            </div>
        </template>
        <template #footer>
            <RouterLink
                :to="{
                    name: 'project',
                    params: {
                        courseId: course.id,
                        projectId: project.id,
                    },
                }"
            >
                <Button :icon="PrimeIcons.ARROW_RIGHT" :label="t('components.card.open')" icon-pos="right" outlined />
            </RouterLink>
        </template>
    </Card>
</template>

<style lang="scss">
@import '@/assets/scss/theme/theme.scss';
.icon-color {
    color: $primaryColor;
    font-size: $fontSize;
}

.border-round {
    border-radius: $borderRadius;
}

.project-card {
    border-style: solid;
    border-width: $borderWidth;
    border-color: $primaryLightColor;

    .p-card-body {
        background: white;
    }
    .p-card-header {
        padding: $cardBodyPadding;
        background: $primaryLightColor;
    }
    .p-card-content {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
}
</style>
