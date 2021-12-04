<template>
  <div class="space">
    <div class="film d-flex align-items-center">
      <div class="whiteBox mx-2" v-for="(n, idx) in range" :key="idx"></div>
    </div>
    <div @click="goToMovieDetail" class="poster d-flex flex-column align-items-center justify-items-center">
      <img :src="posterPath" :alt="`${nowItem.title} 포스터`" height="250px">
      <div>{{ nowItem.title }}</div>
    </div>
    <div class="film d-flex align-items-center">
      <div class="whiteBox mx-2" v-for="(n, idx) in range" :key="idx"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NowMovieItem',
  data() {
    return {
      posterPath: `https://image.tmdb.org/t/p/w500${this.nowItem.poster_path}`,
      range: 6,
    }
  },
  props: {
    nowItem: Object
  },
  methods: {
    goToMovieDetail() {
      this.$router.push({ name: 'MovieDetail', params: { movieId: this.nowItem.id } })
    }
  }
}
</script>

<style scoped>
.space { 
  height: 400px;
  width: 400px;
}
.space{
  animation:text-scroll 25s linear infinite;
}
@keyframes text-scroll{
  from{
    transform:translateX(20%);
    -moz-transform:translateX(20%);
    -webkit-transform:translateX(20%);
    -o-transform:translateX(20%);
    -ms-transform:translateX(20%);
  }
  to{
    transform:translateX(-100%);
    -moz-transform:translateX(-100%);
    -webkit-transform:translateX(-100%);
    -o-transform:translateX(-100%);
    -ms-transform:translateX(-100%);
  }
}
.film {
  background-color: black;
  height: 30px;
}
.whiteBox {
  width: 13px;
  height: 13px;
  background-color: white;
}
.poster {
  height: 300px;
  border-left-style: solid;
  border-width: 20px;
  border-color: black;
}
</style>