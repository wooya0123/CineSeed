<template>
    <div class="modal-overlay gray6">
      <div class="modal-content">
        <!-- ApplicationData가 배열이고 데이터가 있을 경우 -->
        <ul v-if="ApplicationData && ApplicationData.length">
          <li 
            v-for="(data, index) in ApplicationData" 
            :key="index">
            <ul v-if="data.applicants.length">
              <li v-for="applicant in data.applicants">
                <h3 @click="() => goProfile(applicant.id)">
                    {{ applicant.nickname }}
                </h3>
                <p>
                    | {{ data.movieTitle }}
                </p>
                <hr>
              </li>
            </ul>
            <p v-else>아직 지원자가 없습니다.</p>
          </li>
        </ul>
        <!-- 데이터가 없을 경우 -->
        <p v-else>지원 데이터가 없습니다.</p>
        <button class="btn-lg bg-gray5" @click="$emit('close')">닫기</button>
      </div>
    </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account';
import axios from 'axios';
import { defineProps, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// 부모 컴포넌트로부터 데이터 받기
defineProps({
ApplicationData: {
    type: Array,
    required: true,
},
});

const router = useRouter()

const goProfile = (id) => {
    router.push({ 
        name: 'profile', 
        params: { id } // :id에 전달할 값
    })
}
</script>

<style scoped>
.modal-overlay {
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
background: rgba(0, 0, 0, 0.5);
display: flex;
justify-content: center;
align-items: center;
}

.modal-content {
background: white;
padding: 20px;
border-radius: 8px;
max-width: 500px;
}

ul {
list-style: none;
padding: 0;
}

li {
margin: 5px 0;
display: flex;
flex-direction: row;
gap: 20px;
}

h3 {
    cursor: pointer;
}
</style>
