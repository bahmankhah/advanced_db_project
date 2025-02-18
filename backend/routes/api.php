<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AppController;
use App\Http\Controllers\CategoryController;
use App\Models\App;
use Illuminate\Support\Facades\DB;

Route::get('categories', [CategoryController::class, 'index']);

Route::get('content-ratings', function (Request $request) {
    $contentRatings = App::select('content_rating')
        ->whereNotNull('content_rating')
        ->distinct()
        ->get()
        ->pluck('content_rating')
        ->toArray();

    return response()->json($contentRatings);
});

Route::get('/apps', [AppController::class, 'index']);
Route::get('/apps/{id}', [AppController::class, 'show']);
Route::post('/apps', [AppController::class, 'store']);
Route::put('/apps/{id}', [AppController::class, 'update']);
Route::delete('/apps/{id}', [AppController::class, 'destroy']);


Route::get('/ratings-distribution', function (Request $request) {
    $distribution = DB::table('ratings_distribution')
        ->select('rating', 'count')
        ->orderBy('rating')
        ->get();

    return response()->json($distribution);
});

Route::get(
    '/average-ratings',
    function (Request $request) {
        $averages = DB::table('average_ratings_by_category')
            ->select('category_name', 'average_rating')
            ->orderBy('category_name')
            ->get();

        return response()->json($averages);
    }
);
