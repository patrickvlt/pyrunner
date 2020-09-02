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
            $console->info('Installing Pyrunner requirements. This might take a minute.');
            exec('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt', $output, $return);
            if ($return != 0) {
                $console->info('Installing Pyrunner requirements with pip3 instead of pip. This might take a minute.');
                exec('pip3 install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt', $outputTwo, $returnTwo);
                if ($returnTwo != 0) {
                    $console->error('Installing requirements failed. Please run: pip(3) install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt');
                } else {
                    exec('pip3 install chromedriver-py --force-reinstall', $output, $return);
                    $console->info('Succesfully installed Pyrunner requirements.');
                }
            } else {
                exec('pip install chromedriver-py --force-reinstall', $output, $return);
                $console->info('Succesfully installed Pyrunner requirements.');
            }
            if ($console->confirm('Do you want to copy an example file with Pyrunner tests to your project root?')){
                if (!copy('vendor/pveltrop/pyrunner/_tests_example.py', '_tests.py')) {
                    $console->error('Failed to copy vendor/pveltrop/pyrunner/_tests_example.py file.');
                    $console->line('Please refer to the documentation: https://github.com/43874/pyrunner');
                }
            }
            if ($console->confirm('Do you want to copy an example GitLab CI file to your project root?')){
                if (!copy('vendor/pveltrop/pyrunner/.gitlab-ci.yml', '.gitlab-ci.yml')) {
                    $console->error('Failed to copy vendor/pveltrop/pyrunner/.gitlab-ci.yml file.');
                    $console->line('Please refer to the documentation: https://github.com/43874/pyrunner');
                }
            }
            if ($console->confirm('Do you want to generate a .env.example and .env.testing file from your .env? .env.testing is necessary for Gitlab CI/CD.')){
                exec('php artisan pyrunner:env');
                $console->info('Generated example and testing ENVs.');
            }
            $console->info('Succesfully installed Pyrunner. Available commands:');
            $console->line('php artisan pyrunner:install');
            $console->line('php artisan pyrunner:env');
            $console->line('php artisan pyrunner:start');
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
