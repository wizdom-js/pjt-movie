<template>
  <div>
    <iframe :src="getVideoURI()" frameborder="0" width="100%" height="400px" class="mt-5"></iframe>
    <h3 class="text-center my-5">{{ representVideo.name }}</h3>
    <!-- <div>예고편을 준비중입니다</div> -->
    <movie-video-c-list
      v-if="notRVideos"
      :cVideoList="notRVideos"
      @select-video="onSelectVideo"
    ></movie-video-c-list>
  </div>
</template>

<script>
import MovieVideoCList from '@/components/movie/MovieVideoCList'
import _ from 'lodash'

export default {
  name: 'MovieVideos',
  components: {
    MovieVideoCList
  },
  data() {
    return {
      notRVideos: [],
      representVideo: '',
      videoAllList: this.videoList
    }
  },
  props: {
    videoList: Array
  },
  methods: {
    getVideoURI() {
      return `https://www.youtube.com/embed/${this.representVideo.video_id}`
    },
    onSelectVideo(video) {
      this.representVideo = video
    },
    chooseRVideo() { // 대표 메인 비디오 골라내기
      const order = _.reverse(this.videoAllList)
      this.representVideo = order[0]
      this.notRVideos = order
    }
  },
  watch: {
    videoList() {
      this.videoAllList = this.videoList
      this.chooseRVideo()
    }
  },
  created() {
    this.chooseRVideo()
  }

}
</script>

<style>

</style>