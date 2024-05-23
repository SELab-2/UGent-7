<script setup lang="ts">
import Button from 'primevue/button';
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import Title from '@/views/layout/Title.vue';
import Illustration from '@/assets/img/auth/illustration.png';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import { endpoints } from '@/config/endpoints.ts';

const { t } = useI18n();
</script>

<template>
    <BaseLayout>
        <div class="flex align-items-center" id="wrapper">
            <div class="flex flex-column md:flex-row align-self-center w-12 lg:w-10 mx-auto">
                <div class="w-12 md:w-5 bg-primary text-white p-6">
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
                            id="login"
                        />
                    </a>
                </div>
                <div
                    class="w-12 md:w-7 flex flex-column md:flex-row align-items-center md:align-items-end justify-content-between relative surface-100"
                >
                    <img
                        :src="Illustration"
                        :alt="t('views.login.illustration')"
                        class="w-10rem md:w-15rem m-4 my-5 ml:0 md:ml-7"
                    />
                    <div class="bg-primary text-white p-4 w-full md:w-20rem">
                        <h1 class="mt-0 text-white">
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

<style lang="scss" scoped>
#wrapper {
    min-height: calc(100vh - (150px + 173px + 7rem)) !important;
}
</style>
