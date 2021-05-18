<template>
<el-scrollbar style="height:100%;">
<div id='indexs'>
  <el-row>
    <el-col :span="24"><div class="grid-content bg-purple-dark">
      <Indexcomponents />
      </div></el-col>
  </el-row>
</div>
</el-scrollbar>
</template>

<script>
import Indexcomponents from '@/components/index_model'
export default {
  name: 'indexs',
  components: {
    Indexcomponents
  }
}
</script>

<style>
  .el-row {
    margin-bottom: 20px;
    /* &:last-child {
      margin-bottom: 0;
    } */
  }
  .el-col {
    border-radius: 4px;
  }
  /* .bg-purple-dark {
    background: #99a9bf;
  } */
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .new_warp{
    padding-top: 0;
  }
</style>
