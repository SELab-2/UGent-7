<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-8">
                <div>
                    <Title>
                        {{ t('views.submissions.submission') }}
                    </Title>
                </div>
                <div>
                    <p>
                        {{ t('views.submissions.submissionDescription') }}
                    </p>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
