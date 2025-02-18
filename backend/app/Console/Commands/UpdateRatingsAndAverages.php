<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class UpdateRatingsAndAverages extends Command
{
    protected $signature = 'ratings:update';
    protected $description = 'Update ratings distribution and average ratings by category';

    public function handle()
    {
        try {
            $this->updateRatingsDistribution();
            $this->updateAverageRatingsByCategory();
            $this->info('Ratings distribution and average ratings updated successfully.');
        } catch (\Exception $e) {
            Log::error($e->getMessage());
            throw $e;
        }
    }


    private function updateRatingsDistribution()
    {
        DB::table('ratings_distribution')->truncate();

        $distribution = DB::table('apps')
            ->select('rating', DB::raw('COUNT(*) as count'))
            ->whereNotNull('rating')
            ->groupBy('rating')
            ->get();

        foreach ($distribution as $row) {
            DB::table('ratings_distribution')->insert([
                'rating' => $row->rating,
                'count' => $row->count,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }

    private function updateAverageRatingsByCategory()
    {
        DB::table('average_ratings_by_category')->truncate();

        $averages = DB::table('apps')
            ->join('categories', 'apps.category_id', '=', 'categories.category_id')
            ->select('categories.name as category_name', DB::raw('AVG(apps.rating) as average_rating'))
            ->groupBy('categories.name')
            ->get();

        foreach ($averages as $row) {
            DB::table('average_ratings_by_category')->insert([
                'category_name' => $row->category_name,
                'average_rating' => $row->average_rating,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
}
