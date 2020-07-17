<?php

namespace Pveltrop\PyRunner;

use Illuminate\Console\Command;

class Install extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */

    protected $signature = 'pyrunner:install';

    /**
     * The console command description.
     *
     * @var string
     */

    protected $description = 'Installs PyRunner.';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */

    public function handle()
    {
        $console = $this;

        function Install($console){
            shell_exec('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt');
            shell_exec('cp vendor/pveltrop/pyrunner/_tests_example.py');
            if (!copy('vendor/pveltrop/pyrunner/_tests_example.py', '_tests.py')) {
                $console->error('Failed to copy vendor/pveltrop/pyrunner/_tests_example.py file.');
                $console->line('Please refer to the documentation: https://github.com/43874/pyrunner');
            }
            if (!copy('vendor/pveltrop/pyrunner/.gitlab-ci.yml', '.gitlab-ci.yml')) {
                $console->error('Failed to copy vendor/pveltrop/pyrunner/.gitlab-ci.yml file.');
                $console->line('Please refer to the documentation: https://github.com/43874/pyrunner');
            }
            $console->info('Succesfully installed Pyrunner. Run php artisan pyrunner:test to start testing');
        }

        if ($console->confirm('Do you have Python 3 and Pip installed?')){
            Install($console);
        } else {
            $console->error('Please install Python 3 and Pip first');
            $console->line('https://www.python.org/downloads/release/python-381/');
            $console->line('https://pip.pypa.io/en/stable/installing/');
            if ($console->confirm('Finished installing?')){
                Install($console);
            }
        }
    }
}
