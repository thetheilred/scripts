#!/bin/python3

# TODO: Add license

"""This script is used for password generation
usage: password-generator [-h] [-n LENGTH] [--dontUseSpecials] [-v] [-c COUNT]
options:
  -h, --help            show this help message and exit
  -n LENGTH, --length LENGTH
                        Password length. Must be a positive integer >= 4
  --dontUseSpecials     If set, special symbols are NOT used in generated password
  -v, --debug           If set, output debugging logs
  -c COUNT, --count COUNT
                        Number of passwords to generate

Raises:
    argparse.ArgumentTypeError: If LENGTH < 4
    argparse.ArgumentTypeError: If COUNT < 1

Returns:
    list[string]: list of generated passwords
"""

import argparse
import logging
import random
import os

UTIL_NAME = 'password-generator'

###########################################
# Constants used in password generation   #
###########################################

# Sets of symbols
ALPHA_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_UPPERCASE = ALPHA_LOWERCASE.upper()
DIGITS = '0123456789'
SPECIAL_SYMBOLS = '!$%^()_-+='

# Utility constants defining unions of available symbols
ALL_WITH_SPECIALS = ALPHA_LOWERCASE + ALPHA_UPPERCASE + DIGITS + SPECIAL_SYMBOLS
ALL_WITHOUT_SPECIALS = ALPHA_LOWERCASE + ALPHA_UPPERCASE + DIGITS

# Password contets constraints
MIN_ALPHA_LOWERCASE_COUNT=1
MIN_ALPHA_UPPERCASE_COUNT=1
MIN_DIGITS_COUNT=1
MIN_SPECIALS_COUNT=1

# Utility constants defining minimal length of a password
MIN_LENGTH_WITH_SPECIALS = MIN_ALPHA_LOWERCASE_COUNT + MIN_ALPHA_UPPERCASE_COUNT + MIN_DIGITS_COUNT + MIN_SPECIALS_COUNT
MIN_LENGTH_WITHOUT_SPECIALS = MIN_ALPHA_LOWERCASE_COUNT + MIN_ALPHA_UPPERCASE_COUNT + MIN_DIGITS_COUNT

logger = logging.getLogger(UTIL_NAME)

def configureLogging(debug: bool = False):
  """Utility funciton to configure logging level

  Args:
      debug (bool, optional): If True, sets logging level to debug, otherwise to info. Defaults to False.
  """
  if not debug:
    logging.basicConfig(level=logging.INFO)
  else:
    logging.basicConfig(level=logging.DEBUG)

def length(length: str) -> int:
  """Converts passed string to integer, errors if it not passes validation (>= 4)

  Args:
      length (str): string representation of integer

  Raises:
      argparse.ArgumentTypeError: Error if length is < 4

  Returns:
      int: validated integer
  """
  if int(length) < 4:
    raise argparse.ArgumentTypeError(f'Value {length} is out of range. Must be >= 4')
  return int(length)

def count(count: str) -> int:
  """Converts passed string to integer, errors if it not passes validation (>= 4)

  Args:
      length (str): string representation of integer

  Raises:
      argparse.ArgumentTypeError: Error if length is < 1

  Returns:
      int: validated integer
  """
  if int(count) < 1:
    raise argparse.ArgumentTypeError(f'Value {count} is out of range. Must be >= 1')
  return int(count)

def getArgumentParser() -> argparse.ArgumentParser:
  """Configures and returns argparse.ArgumentParser object for further usage in the script

  Returns:
      argparse.ArgumentParser: object that can parse cli arguments
  """
  argumentParser = argparse.ArgumentParser(
    prog=UTIL_NAME,
    description='Generates secure password'
  )
  argumentParser.add_argument(
    '-n', 
    '--length', 
    default=8, 
    type=length, 
    help='Password length. Must be a positive integer >= 4'
  )
  argumentParser.add_argument(
    '--dontUseSpecials', 
    default=False, 
    action='store_true', 
    help='If set, special symbols are NOT used in generated password'
  )
  argumentParser.add_argument(
    '-v',
    '--debug',
    default=False,
    action='store_true',
    help='If set, output debugging logs'
  )
  argumentParser.add_argument(
    '-c',
    '--count',
    default=1,
    type=count,
    help='Number of passwords to generate'
  )
  return argumentParser

def generatePassword(length: int, useSpecials: bool = True) -> str:
  """Generates password of provided length

  Args:
      length (int): Desired length of generated password
      useSpecials (bool, optional): If False, special symbols will not be used in password. 
      Defaults to True.

  Returns:
      str: Generated password
  """
  password = []
  rnd = random.SystemRandom()
  # Add neccessary elements (according to MIN_* consts)
  password.extend([rnd.choice(ALPHA_LOWERCASE) for _ in range(MIN_ALPHA_LOWERCASE_COUNT)])
  password.extend([rnd.choice(ALPHA_UPPERCASE) for _ in range(MIN_ALPHA_UPPERCASE_COUNT)])
  password.extend([rnd.choice(DIGITS) for _ in range(MIN_DIGITS_COUNT)])
  if useSpecials:
    password.extend([rnd.choice(SPECIAL_SYMBOLS) for _ in range(MIN_SPECIALS_COUNT)])
  
  # Add remaining symbols to end up with len(password) == length
  if useSpecials:
    password.extend([rnd.choice(ALL_WITH_SPECIALS) for _ in range(length - MIN_LENGTH_WITH_SPECIALS)])
  else:
    password.extend([rnd.choice(ALL_WITHOUT_SPECIALS) for _ in range(length - MIN_LENGTH_WITHOUT_SPECIALS)])
  
  rnd.shuffle(password)
  return ''.join(password)

def main():
  """Script entrypoint
  """
  parser = getArgumentParser()
  args = parser.parse_args()
  configureLogging(args.debug)
  logging.debug(args)
  print(os.linesep.join([generatePassword(length=args.length, useSpecials=not args.dontUseSpecials) for _ in range(args.count)]))

if __name__ == '__main__':
  main()
