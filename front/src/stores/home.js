import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useHomeStore = defineStore('home', () => {
  const popularMovies = ref([])
  const personalizedMovies = ref([])

  const getPopularMovies = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movie/popular-recommandation/'
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
    const token = localStorage.getItem('user-token')
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movie/personalized-recommandation/',
      // headers: {
      //   'Authorization': `Token c4b9b646d27275ac557b808bf374d0c9a915f8fe`
      // }
    })
      .then((response) => {
        console.log(response)
        personalizedMovies.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  return { popularMovies, personalizedMovies, getPopularMovies, getPersonalizedMovies }
})
  