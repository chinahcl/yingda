<template>
<div class="batch_add_unit">
  <!-- :action="doUpload"    :data="pppss"-->
  <el-row>
  <el-col :span="8"><div class="grid-content bg-purple">
    <el-upload
  accept=".xls,.xlsx,.txt"
  class="upload-demo"
  drag
  :action="doUpload"
  :data="pppss"
  :on-success="handleSuccess"
  multiple>
  <i class="el-icon-upload"></i>
  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
  <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
</el-upload>
    </div></el-col>
  <el-col :span="16"><div class="grid-content bg-purple-light">
    <el-table
      :data="tableData"
      height="740"
      style="width: 100%"
      :default-sort ="{prop:'created_time',order:'descending'}">
      <el-table-column
        sortable
        prop= "created_time"
        label="日期"
        :sort-orders="['descending','ascending']"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        width="100">
      </el-table-column>
      <el-table-column
        prop="w_name"
        label="文件名称"
        width="300">
      </el-table-column>
    <el-table-column
      fixed="right"
      label="操作"
      width="100">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
      </template>
    </el-table-column>
    </el-table>
    </div></el-col>
</el-row>

  <!-- <div class="table_x"> -->
<el-dialog :visible.sync="editFormVisible" width="50%" @click="closeDialog('editForm')">
      <el-form label-width="120px" :model="editForm" ref="editForm">
        <el-row>
          <el-col :span="12">
            <el-form-item label="日期">
              <el-input size="small" v-model="editForm.created_time" ></el-input>
            </el-form-item>
            <el-form-item label="姓名">
              <el-input size="small" v-model="editForm.name"></el-input>
            </el-form-item>
            <el-form-item label="文件名称">
              <el-input size="small" v-model="editForm.w_name"></el-input>
            </el-form-item>
            <el-form-item label="地址">
              <el-input size="small" v-model="editForm.file"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-dialog>

</div>
<!-- </div> -->
</template>

<script>
export default {
  name: 'batch_add_unit',
  data () {
    return {
      editFormVisible: false,
      tableData: [{
        created_time: '',
        name: '',
        file: '',
        w_name: ''
      }],
      doUpload: 'posts',
      pppss: {
        name: localStorage.yun_user.replace('"', '').replace('"', '')
      },
      editForm: {
        address: '1'
      }
    }
  },
  created () {
    this.axios.get('posts', {
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
    handleSuccess () {
      console.log('111')
      location.reload()
    },
    handleClick (row) {
      this.editFormVisible = true
      this.editForm.created_time = row.created_time
      this.editForm.name = row.name
      this.editForm.file = row.file
      this.editForm.w_name = row.w_name
      console.log(row)
      // console.log('code,222')
    }
  }
}
</script>

<style scoped>
.batch_add_unit {
  line-height:55px;
  position:absolute;left:300px;top:200px;
}
.table_x {
  line-height:55px;
  position:absolute;left:200%;top:0px;
}
.row-bg {
    background: red;
  }
</style>
