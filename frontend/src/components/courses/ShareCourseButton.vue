<script setup lang="ts">
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';
import { PrimeIcons } from 'primevue/api';
import { ref } from 'vue';

/* Composable injections */
const { t } = useI18n();

/* Props */
const props = defineProps<{ course: Course }>();

/* State for the dialog to share a course */
const displayShareCourse = ref(false);

/* Invitation link for the course */
const link = ref<string>('KVC Westerlo');

/* Number of days the invitation link is valid */
const linkDuration = ref<number>(7);

/**
 * Creates an invitation link for the course.
 */
 async function handleShare(): Promise<void> {
    // Show a confirmation dialog
    console.log('Share course');
    displayShareCourse.value = false;
}

/**
 * Copies the invitation link to the clipboard.
 */
function copyToClipboard(): void {
    navigator.clipboard.writeText(link.value).then(() => {
        console.log('Link copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}


</script>

<template>
    <div v-tooltip.top="t('views.courses.share.title')">
        <Button
            :icon="PrimeIcons.SHARE_ALT"
            icon-pos="right"
            class="custom-button"
            style="height: 51px; width: 51px"
            @click="displayShareCourse = true"
            v-if="props.course.private_course"
            />
            <Dialog
            v-model:visible="displayShareCourse"
            class="m-3"
            :draggable="false"
            :contentStyle="{ 'min-width': '50vw', 'max-width': '1080px' }"
            modal
            >
            <template #header>
                <h2 class="my-3 text-primary">
                    {{ t('views.courses.share.title') }}
                </h2>
            </template>
            <template #default>
                <p>
                    {{ t('confirmations.shareCourse') }}
                </p>

                <div class="grid">
                    <div class="flex align-items-center col-12 gap-2">
                        <label for="linkDuration">{{ t('views.courses.share.duration') }}</label>
                        <InputNumber v-model="linkDuration" :min="1" :max="28" />
                    </div>
                </div>

                <div class="grid">
                    <div class="flex align-items-center col-12 gap-2">
                        <label for="link">{{ t('views.courses.share.link') }}</label>
                        <InputText v-model="link" disabled />
                        <Button @click="copyToClipboard()" icon="pi pi-copy" class="p-button-text no-outline" />
                    </div>
                </div>

                <div class="flex justify-content-end gap-2 mt-4">
                    <Button @click="displayShareCourse = false" rounded>{{ t('primevue.cancel') }}</Button>
                    <Button @click="handleShare()" rounded>{{ t('views.courses.share.title') }}</Button>
                </div>
            </template>
            </Dialog>
    </div>
</template>

<style scoped lang="scss">
.no-outline:focus,
.no-outline:active {
    box-shadow: none !important;
    
}
</style>