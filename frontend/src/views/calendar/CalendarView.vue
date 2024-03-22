<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Calendar from 'primevue/calendar';
import Title from '@/components/Title.vue';
import moment from 'moment';
import 'moment/dist/locale/nl';
import { computed } from 'vue';
import {useI18n} from 'vue-i18n';
import { ref } from 'vue';

const { t, locale } = useI18n();

/* Keeps track of the selected date */
const selectedDate = ref(new Date());

const formattedDate = computed(() => {
    console.log(locale.value)
    // Format the selected date using moment.js
    return moment(selectedDate.value).locale(locale.value).format('DD MMMM YYYY');
});

</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-6">
                <!-- Calendar heading -->
                <Title class="mb-6">{{ t('views.calendar.title') }}</Title>

                <div>
                    <!-- Calendar itself -->
                    <Calendar class="w-full" v-model="selectedDate" inline/>
                </div>
            </div>
            <div class="col-12 md:col-6">
                <!-- Selected date on the calendar -->
                <Title class="mb-6">{{ formattedDate }}</Title>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>