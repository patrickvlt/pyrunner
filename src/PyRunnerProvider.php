<?php

namespace Pveltrop\PyRunner;

use Illuminate\Support\ServiceProvider;

class PyRunnerProvider extends ServiceProvider
{
    protected $commands = [
        'Pveltrop\PyRunner\Commands\Install',
    ];

    public function register(){
        $this->commands($this->commands);
    }
}
