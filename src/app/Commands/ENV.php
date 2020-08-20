<?php

namespace Pveltrop\PyRunner;

use Illuminate\Console\Command;

class ENV extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */

    protected $signature = 'pyrunner:env';

    /**
     * The console command description.
     *
     * @var string
     */

    protected $description = 'Generates a .env.example and .env.testing from your current .env, without sensitive credentials.';

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
        $env = file_get_contents('.env');

        $newEnv = '';

        function CleanRow($row){
            if (!preg_match('/.*MIX_/i', $row)){
                $valToClean = explode('=',$row)[1];
                $row = str_replace($valToClean,'',$row);
                $row = str_replace('==','=',$row);
            }
            return $row;
        }
        foreach (explode("\n",$env) as $row){
            if (preg_match('/.*_KEY/i', $row)){
                $row = CleanRow($row);
            }
            if (preg_match('/.*_TOKEN/i', $row)){
                $row = CleanRow($row);
            }
            if (preg_match('/.*_SECRET/i', $row)){
                $row = CleanRow($row);
            }
            if (preg_match('/.*_PASSWORD/i', $row)){
                $row = CleanRow($row);
            }
            $newEnv .= $row."\n";
        }

        file_put_contents(".env.example",$newEnv);
        file_put_contents(".env.testing",$newEnv);
        $console = $this;
        $console->info('Generated a new .env.example and .env.testing, replace anything you dont want in source control.');
        $console->info('Excluded keys by default are _TOKEN, _SECRET, _PASSWORD and _KEY.');
    }
}
