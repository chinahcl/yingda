<template>
<!-- <el-scrollbar style="height:70%;"> -->
  <el-table :data="tableData" style="width: 100%;line-height: 40px;" :row-class-name="tableRowClassName">
    <el-table-column prop="unit_name" label="单位名称" width="180"></el-table-column>
    <el-table-column prop="unit_abb" label="单位简称" width="180"></el-table-column>
    <el-table-column prop="use" label="联系人"></el-table-column>
    <el-table-column prop="phone" label="联系电话"></el-table-column>
    <el-table-column prop="iphone" label="手机号"></el-table-column>
    <el-table-column prop="address" label="办公地址"></el-table-column>
    <el-table-column label="状态">
      <template slot-scope="scope">
            <el-tag type="success" effect="dark" v-if="scope.row.userxu==1">正常</el-tag>
            <el-tag type="danger" effect="dark" v-if="scope.row.userxu==2">停用</el-tag>
            <!-- <el-tag type="danger" effect="dark" v-if="scope.row.userxu==3">删除</el-tag> -->
        </template>
    </el-table-column>
  </el-table>
<!-- </el-scrollbar> -->
</template>

<script>
export default {
  name: 'query_unit',
  // created () {
  //   // 获取分类列表
  //   this.open()
  //   this.newdata = []
  // },
  data () {
    return {
      tableData: []
    }
  },
  created () {
    // console.log('新增store', this.$store.state.user.nm)
    // this.$store.commit('user/USER_NAME', '')
    // console.log('新增store---->>>>', this.$store.state.user.nm)
    this.axios.get('/users', {
    }).then((res) => {
      this.tableData = res.data.data
      console.log(res.data.data)
      // console.log('user.id', this.$store.state.user.nm)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex % 2 === 1) {
        return 'success-row'
      }
      // if (rowIndex === 1) {
      //   return 'warning-row'
      // } else if (rowIndex === 3) {
      //   return 'success-row'
      // } else if (rowIndex === 5) {
      //   return 'warning-row'
      // } else if (rowIndex === 7) {
      //   return 'success-row'
      // } else if (rowIndex === 9) {
      //   return 'warning-row'
      // } else if (rowIndex === 11) {
      //   return 'success-row'
      // } else if (rowIndex === 13) {
      //   return 'warning-row'
      // } else if (rowIndex === 15) {
      //   return 'success-row'
      // }
      // return ''
    }
  }
}
</script>

<style scoped>
.el-table >>> .warning-row {
  background: oldlace;
}

.el-table >>> .success-row {
  background: #f0f9eb;
}
/* .el-table__header tr,
.el-table__header th {
  padding: 0;
  height: 30px;
  line-height: 40px;
}
.el-table__body tr,
.el-table__body td {
  padding: 0;
  height: 30px;
  line-height: 30px;
} */
</style>
