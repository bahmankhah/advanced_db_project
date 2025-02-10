<?php

namespace App\Http\Controllers;

use App\Models\App;
use Illuminate\Http\Request;

class AppController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request)
    {
        $query = App::select('categories.name as category_name', 'apps.app_id', 'apps.app_name', 'apps.rating', 'apps.price', 'apps.content_rating')
            ->join('categories', 'apps.category_id', '=', 'categories.category_id');

        if ($request->has('category')) {
            $categoryName = $request->input('category');
            $query->whereHas('category', function ($q) use ($categoryName) {
                $q->where('name', $categoryName);
            });
        }

        if ($request->has('rating')) {
            $query->where('rating', '>=', $request->input('rating'));
        }

        if ($request->has('price')) {
            $query->where('price', '<=', $request->input('price'));
        }

        if ($request->has('content_rating')) {
            $query->where('content_rating', $request->input('content_rating'));
        }

        // Implement pagination (fetch 50 rows per page by default)
        $perPage = $request->input('per_page', 50);
        $apps = $query->paginate($perPage, ['app_id', 'app_name', 'rating', 'price', 'content_rating']);

        return response()->json($apps,);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'app_name' => 'required|string|max:255',
            'category_id' => 'required|exists:categories,category_id',
            'rating' => 'required|numeric|between:0,5',
            'price' => 'required|numeric|between:0,100',
            'content_rating' => 'required|string|in:Everyone,Low Maturity,Mature 17+,Adults Only 18+',
        ]);

        $app = App::create($validatedData);

        return response()->json($app, 201);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, App $app)
    {
        $validatedData = $request->validate([
            'app_name' => 'required|string|max:255',
            'category_id' => 'required|exists:categories,category_id',
            'rating' => 'required|numeric|between:0,5',
            'price' => 'required|numeric|between:0,100',
            'content_rating' => 'required|string|in:Everyone,Low Maturity,Mature 17+,Adults Only 18+',
        ]);

        $app->update($validatedData);

        return response()->json($app);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(App $app)
    {
        $app->delete();

        return response()->json(null, 204);
    }
}
