<script setup lang="ts">
import Button from 'primevue/button';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import Illustration from '@/assets/img/auth/illustration.png';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import { endpoints } from '@/config/endpoints.ts';

const { t } = useI18n();
</script>

<template>
    <BaseLayout>
        <div class="flex pb-7 h-full">
            <div class="flex flex-column md:flex-row align-self-center w-12 lg:w-10 mx-auto">
                <div class="w-12 md:w-5 bg-primary text-white p-5">
                    <Title color="contrast">
                        {{ t('views.login.title') }}
                    </Title>
                    <div class="mb-4 mt-3">
                        {{ t('views.login.subtitle') }}
                    </div>
                    <a :href="endpoints.auth.login">
                        <Button
                            icon-pos="right"
                            :icon="PrimeIcons.ARROW_RIGHT"
                            :label="t('views.login.button')"
                            severity="secondary"
                        />
                    </a>
                </div>
                <div class="w-12 md:w-7 flex flex-column md:flex-row align-items-center md:align-items-end justify-content-between relative surface-100">
                    <img :src="Illustration" :alt="t('views.login.illustration')" class="w-10rem md:w-15rem m-4 ml-7" />
                    <div
                        class="bg-primary text-white p-4 w-full md:w-20rem"
                    >
                        <h1 class="mt-0">
                            {{ t('views.login.card.title') }}
                        </h1>
                        <span>
                        {{ t('views.login.card.subtitle') }}
                    </span>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style lang="scss">

</style>
