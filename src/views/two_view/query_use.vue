<template>
  <el-table :data="tableData" style="width: 100%;line-height: 40px;" :row-class-name="tableRowClassName">
    <el-table-column prop="username" label="姓名" width="80"></el-table-column>
    <el-table-column prop="use_unit" label="单位名称" width="110"></el-table-column>
    <el-table-column prop="use_id" label="身份证号"></el-table-column>
    <el-table-column prop="ment" label="部门"></el-table-column>
    <el-table-column prop="unit_phone" label="办公电话"></el-table-column>
    <el-table-column prop="chu_name" label="处室名称"></el-table-column>
    <el-table-column prop="use_iphone" label="手机"></el-table-column>
    <el-table-column prop="use_address" label="办公地址"></el-table-column>
    <el-table-column label="状态">
      <template slot-scope="scope">
            <el-tag type="success" effect="dark" v-if="scope.row.is_active==0">正常</el-tag>
            <el-tag type="danger" effect="dark" v-if="scope.row.is_active==1">停用</el-tag>
            <!-- <el-tag type="danger" effect="dark" v-if="scope.row.userxu==3">删除</el-tag> -->
        </template>
    </el-table-column>
  </el-table>
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
    const id = localStorage.use_unit
    this.axios.get('/login_dev/reight/query_use/' + id, {
    }).then((res) => {
      // if(res.data)
      // Message.success('登陆成功')
      this.tableData = res.data.data
      console.log(res.data.data)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex === 1) {
        return 'warning-row'
      } else if (rowIndex === 3) {
        return 'success-row'
      } else if (rowIndex === 5) {
        return 'warning-row'
      } else if (rowIndex === 7) {
        return 'success-row'
      } else if (rowIndex === 9) {
        return 'warning-row'
      } else if (rowIndex === 11) {
        return 'success-row'
      } else if (rowIndex === 13) {
        return 'warning-row'
      } else if (rowIndex === 15) {
        return 'success-row'
      }
      return ''
    }
  }
}
</script>

<style scoped>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
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
