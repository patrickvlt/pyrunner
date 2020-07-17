<?php

namespace Pveltrop\PyRunner;

use Illuminate\Console\Command;

class Update extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */

    protected $signature = 'pyrunner:update';

    /**
     * The console command description.
     *
     * @var string
     */

    protected $description = 'Updates PyRunner.';

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
        $console->info('Updating Pyrunner requirements with pip. This might take a minute.');
        exec('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt', $output, $return);
        if ($return != 0) {
            $console->info('Updating Pyrunner requirements with pip3 instead of pip. This might take a minute.');
            exec('pip3 install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt', $outputTwo, $returnTwo);
            if ($returnTwo != 0) {
                $console->error('Updating requirements failed. Please run: pip(3) install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt');
            } else {
                $console->info('Succesfully updated Pyrunner requirements.');
            }
        } else {
            $console->info('Succesfully updated Pyrunner requirements.');
        }

        $console->info('Updating PyRunner core. This might take a minute.');
        $cmd = 'python vendor/pveltrop/pyrunner/_update.py';
        exec($cmd, $output, $returnTwo);
        if ($returnTwo != 0){
            $cmd = 'python3 vendor/pveltrop/pyrunner/_update.py';
            exec($cmd, $output, $returnTwo);
            if ($returnTwo != 0){
                $console->error('Can\'t update PyRunner core files. Check your internet connection.')
            }
        }
    }
}
