<script setup lang="ts">
import Button from 'primevue/button';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import Illustration from '@/assets/img/auth/illustration.png';
import {useI18n} from 'vue-i18n';
import {PrimeIcons} from 'primevue/api';
import {endpoints} from '@/config/endpoints.ts';

const { t } = useI18n();
</script>

<template>
    <BaseLayout>
        <div class="flex w-12 lg:w-10 mx-auto mb-8">
            <div class="w-5 bg-primary text-white p-5">
                <Title color="contrast">
                    {{ t('views.login.title') }}
                </Title>
                <div class="mb-4 mt-3">
                    {{ t('views.login.subtitle') }}
                </div>
                <a :href="endpoints.auth.login">
                    <Button icon-pos="right" :icon="PrimeIcons.ARROW_RIGHT" :label="t('views.login.button')" severity="secondary"/>
                </a>
            </div>
            <div class="w-7 relative surface-100 p-4">
                <img :src="Illustration" :alt="t('views.login.illustration')" class="w-15rem"/>
                <div class="absolute bottom-0 right-0 bg-primary text-white p-4 w-20rem" style="transform: translateY(50%);">
                    <h1 class="mt-0">
                        {{ t('views.login.card.title') }}
                    </h1>
                    <span>
                        {{ t('views.login.card.subtitle') }}
                    </span>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>