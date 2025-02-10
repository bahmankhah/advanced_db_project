<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class App extends Model
{
    protected $primaryKey = 'app_id';

    // protected $appends = ['category_name'];

    public function category(){
        return $this->belongsTo(Category::class, 'category_id', 'category_id');
    }



    public function developer(){
        return $this->belongsTo(Developer::class, 'developer_id', 'developer_id');
    }


}
