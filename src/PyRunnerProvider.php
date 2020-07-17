<?php

namespace Pveltrop\PyRunner;

use Pveltrop\PyRunner\Install;
use Pveltrop\PyRunner\Start;
use Illuminate\Support\ServiceProvider;

class PyRunnerProvider extends ServiceProvider
{
    public function boot()
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            Install::class,
            Start::class,
            Update::class,
        ]);
    }
}
}
