import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/account'

export const useHomeStore = defineStore('home', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const popularMovies = ref([])
  const personalizedMovies = ref([])

  const getPopularMovies = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movie/popular-recommandation/`
    })
      .then((response) => {
        console.log(response)
        popularMovies.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
  const getPersonalizedMovies = function () {
    const account = useAccountStore()
    const token = account.token
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movie/personalized-recommandation/`,
      headers: {
        'Authorization': `Token ${token}`
      }
    })
      .then((response) => {
        personalizedMovies.value = response.data
      })
      .catch((error) => {
        console.log(token)
        console.log('로그인하지 않은 사용자입니다.')
      })
  }

  return { popularMovies, personalizedMovies, getPopularMovies, getPersonalizedMovies }
})
  