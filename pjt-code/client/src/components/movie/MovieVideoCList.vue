<template>
  <v-expansion-panels>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Other Trailers
      </v-expansion-panel-header>
      <v-expansion-panel-content class="my-3">
        <movie-video-c-item
          v-for="cVideo in propcVideoList"
          :key=cVideo.video_id
          :video="cVideo"
          @select-video="onSelectVideo"
        ></movie-video-c-item>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import MovieVideoCItem from '@/components/movie/MovieVideoCItem'

export default { 
  name: 'MovieVideoCList',
  components: {
    MovieVideoCItem
  },
  props: {
    cVideoList: Array,
  },
  data() {
    return {
      propcVideoList: this.cVideoList
    }
  },
  methods: {
    onSelectVideo(video) {
      this.$emit('select-video', video)
    }
  },
  watch: {
    cVideoList() {
      this.propcVideoList = this.cVideoList
    }
  }

}
</script>

<style>

</style>