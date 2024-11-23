<template>
  <div>
    {{ account.profile}}
  </div>
</template>

<script setup>
import MovieCarousel from '@/components/MovieCarousel.vue';

import { useAccountStore } from '@/stores/account';
import { onMounted } from 'vue';

const account = useAccountStore()

onMounted(() => {
  console.log(account.profile)
  account.myPage()
})
</script>

<style scoped>

</style>