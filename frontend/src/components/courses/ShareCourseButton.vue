<script setup lang="ts">
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';
import { PrimeIcons } from 'primevue/api';
import { ref, computed } from 'vue';
import { useCourses } from '@/composables/services/course.service';
import Editor from '@/components/forms/Editor.vue';

/* Composable injections */
const { t } = useI18n();
const { activateInvitationLink } = useCourses();

/* Props */
const props = defineProps<{ course: Course }>();

/* State for the dialog to share a course */
const displayShareCourse = ref(false);

/* Number of days the invitation link is valid */
const linkDuration = ref<number>(7);

/**
 * Activates the invitation link for the course, with the specified duration.
 */
async function handleShare(): Promise<void> {
    // Activates the invitation link by setting an expiration date
    await activateInvitationLink(props.course.id, linkDuration.value);

    // Close the dialog
    displayShareCourse.value = false;
}

/**
 * Copies the invitation link to the clipboard.
 */
function copyToClipboard(): void {
    navigator.clipboard.writeText(invitationLink.value);
}

/**
 * Returns the course's invitation link, formatted as the full URL.
 */
const invitationLink = computed(() => {
    return `${window.location.toString()}/join/${props.course.invitation_link}`;
});
</script>

<template>
    <div v-tooltip.top="t('views.courses.share.title')">
        <Button
            :icon="PrimeIcons.SHARE_ALT"
            icon-pos="right"
            class="custom-button"
            style="height: 51px; width: 51px"
            @click="displayShareCourse = true"
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
                    <!-- Link duration -->
                    <div class="field col">
                        <label for="linkDuration">{{ t('views.courses.share.duration') }}</label>
                        <InputNumber v-model="linkDuration" :min="1" :max="28" />
                    </div>
                </div>

                <div class="grid">
                    <div class="field col">
                        <label for="link">{{ t('views.courses.share.link') }}</label>
                        <div class="flex">
                            <InputText v-model="invitationLink" disabled/>
                            <Button @click="copyToClipboard()" icon="pi pi-copy" class="p-button-text no-outline" />
                        </div>
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
