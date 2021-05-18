<template>
<div id="use_binding_robot">
  <el-table :data="tableData" style="width: 100%;line-height: 40px;" :row-class-name="tableRowClassName">
    <el-table-column prop="username" label="姓名" width="80"></el-table-column>
    <el-table-column prop="use_unit" label="单位名称" width="110"></el-table-column>
    <el-table-column prop="use_id" label="身份证号"></el-table-column>
    <el-table-column prop="ment" label="部门"></el-table-column>
    <el-table-column prop="unit_phone" label="办公电话"></el-table-column>
    <el-table-column prop="chu_name" label="处室名称"></el-table-column>
    <el-table-column prop="use_iphone" label="手机"></el-table-column>
    <el-table-column prop="use_address" label="办公地址"></el-table-column>
    <el-table-column label="编辑">
      <template slot-scope="scope">
        <!-- <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button> -->
        <el-button @click="handleClick(scope.$index, scope.row, tableData)" type="primary" size="small">绑定机器人</el-button>
      </template>
    </el-table-column>
  </el-table>
<!-- <Pagination v-bind:child-msg="pageparm" @callFather="callFather"></Pagination> -->
<!-- <el-dialog :title="title" :visible.sync="editFormVisible" width="50%" @click="closeDialog('editForm')"> -->
<el-dialog :visible.sync="editFormVisible" width="50%" @click="closeDialog('editForm')">
      <el-form label-width="120px" :model="editForm" ref="editForm">
        <el-row>
          <el-col :span="12">
            <el-form-item label="姓名">
              <el-input size="small" v-model="editForm.username" disabled></el-input>
            </el-form-item>
            <el-form-item label="单位名称">
              <el-input size="small" v-model="editForm.use_unit" disabled></el-input>
            </el-form-item>
            <el-form-item label="身份证号">
              <el-input size="small" v-model="editForm.use_id" oninput ="value=value.replace(/[^\d]/g,'')" disabled></el-input>
            </el-form-item>
            <!-- <el-form-item label="处室名称">
              <el-input size="small" v-model="editForm.chu_name" disabled></el-input>
            </el-form-item> -->
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门">
              <el-input size="small" v-model="editForm.ment" disabled></el-input>
            </el-form-item>
            <el-form-item label="办公电话">
              <el-input size="small" v-model="editForm.unit_phone" disabled></el-input>
            </el-form-item>
            <el-form-item label="手机">
              <el-input size="small" v-model="editForm.use_iphone" oninput ="value=value.replace(/[^\d]/g,'')" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
            <el-form-item label="选择绑定机器人">
                <el-checkbox-group v-model="editForm.type">
                <el-checkbox v-for="city in cities" :label="city" :key="city" name="type">{{city}}</el-checkbox>
                </el-checkbox-group>
            </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit()">确认修改</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

</div>
</template>

<script>
import { Message } from 'element-ui'
// import { setTimeout } from 'timers'
export default {
  name: 'use_binding_robot',
  // created () {
  //   // 获取分类列表
  //   this.open()
  //   this.newdata = []
  // },
  data () {
    return {
      name: localStorage.yun_user.replace('"', "'").replace('"', "'"),
      cities: [],
      form: {
        type: []
      },
      tableData: [],
      editFormVisible: false,
      index: '',
      rows: '',
      // title: '预览',
      editForm: {
        type: [],
        id: '',
        username: '',
        use_unit: '',
        use_id: '',
        unit_name: '',
        unit_phone: '',
        // chu_name: '',
        use_iphone: '',
        // use_address: '',
        ment: ''
        // token: localStorage.getItem('logintoken')
      }
    }
  },
  created () {
    const id = localStorage.use_unit
    this.axios.get('/login_dev/reight/query_use/' + id, {
    }).then((res) => {
      this.tableData = res.data.data
      console.log(res.data.data)
    })
    // .catch((error) => {
    //   console.log(error)
    // })
  },
  methods: {
    handleClick (index, row, rows) {
      this.index = index
      this.rows = rows
      this.editFormVisible = true
      this.editForm.id = row.id
      this.editForm.username = row.username
      this.editForm.use_unit = row.use_unit
      this.editForm.use_id = row.use_id
      this.editForm.unit_name = row.unit_name
      this.editForm.unit_phone = row.unit_phone
      this.editForm.chu_name = row.chu_name
      this.editForm.use_iphone = row.use_iphone
      this.editForm.uintstate = row.uintstate
      this.editForm.use_address = row.use_address
      this.editForm.ment = row.ment
      console.log(row)
      // row.unit_id 单位id
      this.axios.get('/robotapi/unit_id/' + row.unit_id, {
      }).then((res) => {
        console.log('x', res.data.data)
        this.cities = res.data.data
      }).catch((error) => {
        console.log(error)
      })
      this.axios.get('/robotapi/use_in_robot/' + row.username, {
      }).then(res => {
        console.log(res)
        this.editForm.type = res.data.data
      })
    },
    onSubmit () {
      console.log('确认绑定')
      const data = this.editForm
      const id = this.editForm.id
      const name = this.name
      console.log(id)
      // const _this = this
      this.axios.post('/robotapi/use_in_robot/' + 'id', {
        data,
        name
      }).then((res) => {
        console.log(res.data.code)
        if (res.data.code === 1) {
        // _this.$router.push('/index_1/change_unit')
          Message.success('修改成功')
          //   this.editFormVisible = false
          //   this.rows.splice(this.index, 1, res.data.data)
          setTimeout(() => { location.reload() }, 800)
        } else {
          Message.warning('用户名或手机号重复！')
        }
      })
    },
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
</style>
