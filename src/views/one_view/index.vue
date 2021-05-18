<template>
    <div>
        <el-carousel :interval="8000" type="card" height="500px" trigger="click" arrow="always">
            <el-carousel-item v-for="item in imgList" :key="item.name">
              <a :href='item.click1'>
                <!-- <h3 class="medium">{{ item }}</h3> -->
                <img style="width:100%;height:100%;" :click='item.click1' :src="item.url" alt="图片丢失了"/>
              </a>
            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
export default {
  data () {
    return {
      imgList: [
        { name: 'lj', url: require('../../assets/login_t.png') },
        { name: 'jj', url: require('../../assets/14.jpg'), click1: '/robot/fa_piao_shi_bie' },
        { name: 'yj', url: require('../../assets/13.jpg'), click1: '/robot/fa_piao_cha_yan' }
      ]
    }
  }
}
//   created() {},
//   mounted() {},
//   computed: {},
//   methods: {}
</script>

<style scoped>
.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>
